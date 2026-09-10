"""
Geofenced Alert Service & SHA-256 OTP Verification for GiriRaksha.
Calculates Haversine distances for 25km geofences and dispatches disaster advisories.
"""

import math
import hashlib
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from database import Subscriber, OtpToken

OTP_SALT = os.getenv("OTP_SALT", "GIRIRAKSHA_SIH_2026_SECRET_KEY")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "alerts@giriraksha.in")


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


def generate_sha256_otp(email: str, db: Session) -> Tuple[str, str]:
    """
    Generates a 6-digit numeric OTP, computes its SHA-256 cryptographic hash,
    and stores it in the database with a 10-minute validity window.
    """
    code = f"{random.randint(100000, 999999)}"
    raw_str = f"{email}:{code}:{OTP_SALT}"
    token_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Invalidate prior unused OTPs for this email
    db.query(OtpToken).filter(OtpToken.email == email, OtpToken.used == False).update({"used": True})

    otp_record = OtpToken(
        email=email,
        token_hash=token_hash,
        code=code,
        expires_at=expires_at,
        used=False
    )
    db.add(otp_record)
    db.commit()

    return code, token_hash


def verify_sha256_otp(email: str, code: str, db: Session) -> bool:
    """Verifies user-provided code against stored SHA-256 hash and expiry."""
    raw_str = f"{email}:{code}:{OTP_SALT}"
    expected_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    record = (
        db.query(OtpToken)
        .filter(
            OtpToken.email == email,
            OtpToken.token_hash == expected_hash,
            OtpToken.used == False
        )
        .first()
    )

    if not record:
        return False

    now_utc = datetime.now(timezone.utc)
    # Ensure tz-aware comparison
    record_exp = record.expires_at
    if record_exp.tzinfo is None:
        record_exp = record_exp.replace(tzinfo=timezone.utc)

    if now_utc > record_exp:
        return False

    record.used = True
    # Mark subscriber as verified
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if subscriber:
        subscriber.verified = True

    db.commit()
    return True


def find_subscribers_in_geofence(
    hazard_lat: float,
    hazard_lon: float,
    radius_km: float,
    db: Session
) -> List[Dict[str, Any]]:
    """Finds all verified subscribers within the hazard's geofenced radius."""
    subscribers = db.query(Subscriber).filter(Subscriber.verified == True).all()
    matched = []

    for sub in subscribers:
        dist = haversine_distance_km(hazard_lat, hazard_lon, sub.lat, sub.lon)
        effective_radius = max(radius_km, sub.radius_km or 25.0)
        if dist <= effective_radius:
            matched.append({
                "email": sub.email,
                "distance_km": dist,
                "location_name": sub.location_name,
                "phone": sub.phone
            })

    return matched


def dispatch_hazard_alert_email(
    subscriber_email: str,
    hazard_data: Dict[str, Any],
    distance_km: float
) -> Dict[str, Any]:
    """
    Dispatches a high-priority early warning HTML email to a geofenced subscriber.
    Falls back to sandbox simulation when SMTP credentials are not present.
    """
    subject = f"[EMERGENCY ALERT] Landslide Hazard Detected within {distance_km} km of Your Location - GiriRaksha"
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px;">
        <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 28px; border: 1px solid #ef4444;">
          <div style="text-align: center; border-bottom: 1px solid #334155; padding-bottom: 16px;">
            <h1 style="color: #ef4444; margin: 0; font-size: 22px;">GIRIRAKSHA EARLY-WARNING ALERT</h1>
            <p style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Smart India Hackathon 2026 | National Mountain Safety System</p>
          </div>
          <div style="margin-top: 20px;">
            <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 14px; border-radius: 6px;">
              <strong style="color: #f87171; font-size: 16px;">CRITICAL HAZARD ZONE NEARBY ({distance_km} km)</strong>
              <p style="margin: 6px 0 0 0; color: #e2e8f0; font-size: 14px;"><strong>Location:</strong> {hazard_data.get('title', 'Mountain Sector')}</p>
              <p style="margin: 4px 0 0 0; color: #e2e8f0; font-size: 14px;"><strong>Corridor:</strong> {hazard_data.get('corridor', 'Highway')}</p>
              <p style="margin: 4px 0 0 0; color: #e2e8f0; font-size: 14px;"><strong>Risk Score:</strong> {hazard_data.get('risk_score', 'High')}/100</p>
            </div>
            <div style="margin-top: 18px; line-height: 1.6; font-size: 14px; color: #cbd5e1;">
              <p><strong>Telemetry Analysis:</strong></p>
              <ul>
                <li>Slope Gradient: {hazard_data.get('slope_deg', 45)}°</li>
                <li>Soil Moisture Saturation: {hazard_data.get('soil_moisture_pct', 85)}%</li>
                <li>3-Day Rainfall Accumulation: {hazard_data.get('rainfall_3d_mm', 120)} mm</li>
              </ul>
              <p><strong>Actionable Recommendations:</strong></p>
              <p style="color: #fca5a5;">{hazard_data.get('road_status', 'Avoid night travel. Keep emergency supplies ready.')}</p>
            </div>
            <div style="margin-top: 24px; padding: 16px; background: #0f172a; border-radius: 8px; text-align: center;">
              <p style="margin: 0; font-size: 12px; color: #94a3b8;">National Disaster Helpline: <strong style="color: #38bdf8;">1078</strong> | State Emergency: <strong style="color: #38bdf8;">112</strong></p>
            </div>
          </div>
        </div>
      </body>
    </html>
    """

    if SMTP_HOST and SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = SMTP_FROM
            msg["To"] = subscriber_email
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_FROM, subscriber_email, msg.as_string())

            return {"status": "SENT", "method": "SMTP_LIVE", "email": subscriber_email}
        except Exception as e:
            return {"status": "FAILED", "error": str(e), "email": subscriber_email}
    else:
        # Sandbox simulated dispatch
        return {
            "status": "SENT_SANDBOX",
            "method": "SIMULATED_POOLED_TRANSPORT",
            "email": subscriber_email,
            "subject": subject,
            "preview_snippet": f"Hazard {hazard_data.get('title')} detected {distance_km} km away."
        }
