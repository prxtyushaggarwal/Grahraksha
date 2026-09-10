"use client";

import React, { useEffect, useRef, useState } from "react";
import { HazardItem, RouteSampleResult } from "@/types";
import { Layers, Globe, Map, AlertTriangle, ShieldCheck, Activity, Maximize2, LocateFixed, Mountain } from "lucide-react";

interface GlobeViewProps {
  hazards: HazardItem[];
  selectedHazard: HazardItem | null;
  onSelectHazard: (h: HazardItem | null) => void;
  routeResult: RouteSampleResult | null;
  onMapClick?: (lat: number, lon: number) => void;
}

export default function GlobeView({
  hazards,
  selectedHazard,
  onSelectHazard,
  routeResult,
  onMapClick,
}: GlobeViewProps) {
  const [viewMode, setViewMode] = useState<"3d" | "2d">("3d");
  const [cesiumLoaded, setCesiumLoaded] = useState(false);
  const cesiumContainerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const routePolylineRef = useRef<any>(null);

  // Load Cesium dynamically from CDN
  useEffect(() => {
    if (typeof window === "undefined") return;

    if ((window as any).Cesium) {
      setCesiumLoaded(true);
      return;
    }

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Widgets/widgets.css";
    document.head.appendChild(link);

    const script = document.createElement("script");
    script.src = "https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Cesium.js";
    script.async = true;
    script.onload = () => {
      setCesiumLoaded(true);
    };
    script.onerror = () => {
      console.warn("Cesium CDN load failed or offline, defaulting to high-performance 2D view.");
      setViewMode("2d");
    };
    document.body.appendChild(script);
  }, []);

  // Initialize Cesium Viewer
  useEffect(() => {
    if (!cesiumLoaded || viewMode !== "3d" || !cesiumContainerRef.current) return;
    const Cesium = (window as any).Cesium;
    if (!Cesium) return;

    try {
      if (!viewerRef.current) {
        const imagery = new Cesium.OpenStreetMapImageryProvider({
          url: "https://tile.openstreetmap.org/"
        });

        const viewer = new Cesium.Viewer(cesiumContainerRef.current, {
          imageryProvider: imagery,
          baseLayerPicker: false,
          geocoder: false,
          homeButton: false,
          infoBox: false,
          selectionIndicator: false,
          timeline: false,
          animation: false,
          navigationHelpButton: false,
          sceneModePicker: false,
          fullscreenButton: false,
        });

        // Focus camera on Indian Himalayas
        viewer.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(78.5, 30.5, 1200000),
          duration: 1.5,
        });

        const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
        handler.setInputAction((click: any) => {
          const pickedObject = viewer.scene.pick(click.position);
          if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.hazardData) {
            onSelectHazard(pickedObject.id.hazardData);
          } else {
            const ray = viewer.camera.getPickRay(click.position);
            const cartesian = viewer.scene.globe.pick(ray, viewer.scene);
            if (cartesian) {
              const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
              const lon = Cesium.Math.toDegrees(cartographic.longitude);
              const lat = Cesium.Math.toDegrees(cartographic.latitude);
              if (onMapClick) onMapClick(Number(lat.toFixed(4)), Number(lon.toFixed(4)));
            }
          }
        }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

        viewerRef.current = viewer;
      }
    } catch (e) {
      console.warn("Error initializing Cesium viewer:", e);
      setViewMode("2d");
    }

    return () => {
      if (viewerRef.current && !viewerRef.current.isDestroyed()) {
        try {
          viewerRef.current.destroy();
          viewerRef.current = null;
        } catch (_) {}
      }
    };
  }, [cesiumLoaded, viewMode]);

  // Update Cesium Hazard Markers
  useEffect(() => {
    const viewer = viewerRef.current;
    const Cesium = (window as any).Cesium;
    if (!viewer || !Cesium || viewMode !== "3d") return;

    markersRef.current.forEach((e) => viewer.entities.remove(e));
    markersRef.current = [];

    hazards.forEach((h) => {
      let pinColor = Cesium.Color.fromCssColorString("#ef4444");
      if (h.severity === "Moderate") pinColor = Cesium.Color.fromCssColorString("#f59e0b");
      if (h.severity === "Low") pinColor = Cesium.Color.fromCssColorString("#22c55e");

      const entity = viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(h.lon, h.lat, 1500),
        point: {
          pixelSize: h.severity === "Severe" ? 18 : 13,
          color: pinColor,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 2,
        },
        label: {
          text: `${h.title}\n[Risk: ${h.risk_score}]`,
          font: "12px sans-serif",
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 2,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          pixelOffset: new Cesium.Cartesian2(0, -28),
          scale: 0.85,
        },
      });
      entity.hazardData = h;
      markersRef.current.push(entity);
    });
  }, [hazards, cesiumLoaded, viewMode]);

  // Update Route Polyline in Cesium
  useEffect(() => {
    const viewer = viewerRef.current;
    const Cesium = (window as any).Cesium;
    if (!viewer || !Cesium || viewMode !== "3d") return;

    if (routePolylineRef.current) {
      viewer.entities.remove(routePolylineRef.current);
      routePolylineRef.current = null;
    }

    if (routeResult && routeResult.segments && routeResult.segments.length > 1) {
      const positions = routeResult.segments.map((seg) =>
        Cesium.Cartesian3.fromDegrees(seg.lon, seg.lat, (seg.elevation_m || 1000) + 100)
      );

      let lineColor = Cesium.Color.fromCssColorString("#22c55e");
      if (routeResult.verdict_badge === "Red") lineColor = Cesium.Color.fromCssColorString("#ef4444");
      else if (routeResult.verdict_badge === "Amber") lineColor = Cesium.Color.fromCssColorString("#f59e0b");

      routePolylineRef.current = viewer.entities.add({
        polyline: {
          positions: positions,
          width: 5,
          material: new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.25,
            color: lineColor,
          }),
        },
      });

      const mid = routeResult.segments[Math.floor(routeResult.segments.length / 2)];
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(mid.lon, mid.lat, 350000),
        duration: 1.5,
      });
    }
  }, [routeResult, cesiumLoaded, viewMode]);

  // Fly to selected hazard
  useEffect(() => {
    const viewer = viewerRef.current;
    const Cesium = (window as any).Cesium;
    if (!viewer || !Cesium || !selectedHazard || viewMode !== "3d") return;

    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(selectedHazard.lon, selectedHazard.lat, 45000),
      duration: 1.2,
    });
  }, [selectedHazard, viewMode]);

  const flyToRegion = (lat: number, lon: number, alt: number = 1000000) => {
    if (viewerRef.current && (window as any).Cesium) {
      const Cesium = (window as any).Cesium;
      viewerRef.current.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(lon, lat, alt),
        duration: 1.4,
      });
    }
  };

  return (
    <div className="relative w-full h-full min-h-[520px] bg-slate-950 rounded-xl overflow-hidden border border-slate-800 shadow-2xl flex flex-col">
      {/* View Switcher Bar */}
      <div className="absolute top-4 left-4 z-20 flex flex-wrap items-center gap-2 bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700 shadow-lg text-xs">
        <span className="text-slate-400 font-semibold uppercase tracking-wider flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          Engine:
        </span>
        <button
          onClick={() => setViewMode("3d")}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md font-medium transition-all ${
            viewMode === "3d"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-sm"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          3D Cesium Globe
        </button>
        <button
          onClick={() => setViewMode("2d")}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md font-medium transition-all ${
            viewMode === "2d"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-sm"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Map className="w-3.5 h-3.5" />
          2D Tactical Grid
        </button>
      </div>

      {/* Regional Camera Focus Buttons */}
      <div className="absolute top-4 right-4 z-20 flex items-center gap-2">
        <button
          onClick={() => flyToRegion(30.5, 78.5, 1100000)}
          className="bg-slate-900/90 backdrop-blur-md hover:bg-slate-800 text-slate-200 text-xs px-2.5 py-1.5 rounded-lg border border-slate-700 flex items-center gap-1.5 shadow-lg transition-all"
        >
          <LocateFixed className="w-3.5 h-3.5 text-cyan-400" />
          Himalayas
        </button>
        <button
          onClick={() => flyToRegion(26.2, 92.8, 900000)}
          className="bg-slate-900/90 backdrop-blur-md hover:bg-slate-800 text-slate-200 text-xs px-2.5 py-1.5 rounded-lg border border-emerald-500/40 text-emerald-300 flex items-center gap-1.5 shadow-lg transition-all"
        >
          <Mountain className="w-3.5 h-3.5 text-emerald-400" />
          Assam / North East
        </button>
      </div>

      {/* 3D Cesium Container */}
      <div
        ref={cesiumContainerRef}
        className={`w-full h-full flex-1 ${viewMode === "3d" ? "block" : "hidden"}`}
      />

      {/* 2D Tactical Fallback Canvas / Map */}
      {viewMode === "2d" && (
        <div className="w-full h-full flex-1 bg-slate-900 relative overflow-hidden flex flex-col items-center justify-center p-6">
          <div className="absolute inset-0 opacity-25 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:16px_16px]" />
          <div className="z-10 max-w-lg w-full bg-slate-800/90 border border-slate-700 p-6 rounded-xl text-center shadow-xl backdrop-blur-md">
            <Map className="w-12 h-12 text-cyan-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white mb-1">Tactical 2D Mountain Grid Active</h3>
            <p className="text-xs text-slate-400 mb-4">
              Displaying high-contrast vector grid for mountain patrol officers and low-bandwidth telemetry field desks.
            </p>
            <div className="grid grid-cols-2 gap-2 text-left text-xs mb-4">
              <div className="bg-slate-900/80 p-2.5 rounded border border-slate-700">
                <span className="text-slate-400 block">Monitored Hazard Pins</span>
                <span className="text-base font-bold text-rose-400">{hazards.length} Active Nodes</span>
              </div>
              <div className="bg-slate-900/80 p-2.5 rounded border border-slate-700">
                <span className="text-slate-400 block">Active Route Corridor</span>
                <span className="text-base font-bold text-cyan-300">
                  {routeResult ? `${routeResult.segments.length} Waypoints` : "Standby"}
                </span>
              </div>
            </div>
            <button
              onClick={() => setViewMode("3d")}
              className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold transition-all shadow-md"
            >
              Switch back to 3D Cesium Globe
            </button>
          </div>
        </div>
      )}

      {/* Selected Hazard Telemetry Overlay Drawer */}
      {selectedHazard && (
        <div className="absolute bottom-6 left-6 right-6 md:right-auto md:w-96 z-20 bg-slate-900/95 backdrop-blur-md border border-rose-500/40 rounded-xl p-4 shadow-2xl animate-in fade-in slide-in-from-bottom-4 duration-200">
          <div className="flex items-start justify-between border-b border-slate-800 pb-2 mb-3">
            <div>
              <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded ${
                selectedHazard.severity === "Severe" ? "bg-rose-500/20 text-rose-400 border border-rose-500/30" : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
              }`}>
                {selectedHazard.severity} Hazard
              </span>
              <h4 className="text-sm font-bold text-white mt-1">{selectedHazard.title}</h4>
              <p className="text-xs text-slate-400">{selectedHazard.corridor}</p>
            </div>
            <button
              onClick={() => onSelectHazard(null)}
              className="text-slate-400 hover:text-white text-sm px-1.5 py-0.5 rounded bg-slate-800"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs mb-3">
            <div className="bg-slate-800/80 p-2 rounded border border-slate-700/60">
              <span className="text-[11px] text-slate-400 block">Susceptibility Risk</span>
              <span className="text-sm font-bold text-rose-400">{selectedHazard.risk_score} / 100</span>
            </div>
            <div className="bg-slate-800/80 p-2 rounded border border-slate-700/60">
              <span className="text-[11px] text-slate-400 block">Slope Angle</span>
              <span className="text-sm font-bold text-amber-300">{selectedHazard.slope_deg}°</span>
            </div>
            <div className="bg-slate-800/80 p-2 rounded border border-slate-700/60">
              <span className="text-[11px] text-slate-400 block">Soil Saturation</span>
              <span className="text-sm font-bold text-cyan-300">{selectedHazard.soil_moisture_pct}%</span>
            </div>
            <div className="bg-slate-800/80 p-2 rounded border border-slate-700/60">
              <span className="text-[11px] text-slate-400 block">3-Day Rainfall</span>
              <span className="text-sm font-bold text-blue-400">{selectedHazard.rainfall_3d_mm} mm</span>
            </div>
          </div>

          <div className="bg-slate-950/70 p-2.5 rounded border border-slate-800 text-[11px] text-slate-300 mb-3">
            <strong className="text-amber-400 block mb-1">Status / Field Note:</strong>
            {selectedHazard.road_status}
          </div>

          <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
            <span>Sensor: {selectedHazard.sensor_status}</span>
            <span>{selectedHazard.last_updated}</span>
          </div>
        </div>
      )}
    </div>
  );
}
