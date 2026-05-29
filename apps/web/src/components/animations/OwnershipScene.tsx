"use client";

import { useRef, useMemo, useEffect } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

// Particle system representing memory cells
function MemoryParticles() {
  const meshRef = useRef<THREE.Points>(null);
  const { size } = useThree();

  const count = 1800;
  const { positions, colors, speeds } = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const speeds = new Float32Array(count);

    const rustOrange = new THREE.Color("oklch(0.68 0.18 42)");
    const dimBlue = new THREE.Color("oklch(0.30 0.04 265)");
    const midGray = new THREE.Color("oklch(0.22 0.02 265)");

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      // Spread across a wide field
      positions[i3]     = (Math.random() - 0.5) * 18;
      positions[i3 + 1] = (Math.random() - 0.5) * 10;
      positions[i3 + 2] = (Math.random() - 0.5) * 8;

      speeds[i] = 0.2 + Math.random() * 0.6;

      // Color: ~15% rust orange, rest dim
      const t = Math.random();
      const col = t < 0.12 ? rustOrange : t < 0.35 ? dimBlue : midGray;
      colors[i3]     = col.r;
      colors[i3 + 1] = col.g;
      colors[i3 + 2] = col.b;
    }
    return { positions, colors, speeds };
  }, []);

  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(positions.slice(), 3));
    g.setAttribute("color",    new THREE.BufferAttribute(colors, 3));
    return g;
  }, [positions, colors]);

  const mat = useMemo(
    () =>
      new THREE.PointsMaterial({
        size: 0.045,
        vertexColors: true,
        transparent: true,
        opacity: 0.85,
        sizeAttenuation: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      }),
    []
  );

  const time = useRef(0);

  useFrame((_, delta) => {
    time.current += delta * 0.3;
    if (!meshRef.current) return;

    const pos = meshRef.current.geometry.attributes.position;
    const arr = pos.array as Float32Array;
    const src = positions;

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      const spd = speeds[i];
      arr[i3 + 1] = src[i3 + 1] + Math.sin(time.current * spd + src[i3] * 0.3) * 0.15;
      arr[i3]     = src[i3]     + Math.cos(time.current * spd * 0.7 + src[i3 + 2] * 0.2) * 0.08;
    }
    pos.needsUpdate = true;

    meshRef.current.rotation.y = time.current * 0.04;
  });

  return <points ref={meshRef} geometry={geo} material={mat} />;
}

// Glowing connection lines — represent ownership transfers
function OwnershipLines() {
  const linesRef = useRef<THREE.LineSegments>(null);
  const time = useRef(0);

  const { positions, colors } = useMemo(() => {
    const nodeCount = 12;
    const nodes: [number, number, number][] = Array.from({ length: nodeCount }, () => [
      (Math.random() - 0.5) * 10,
      (Math.random() - 0.5) * 5,
      (Math.random() - 0.5) * 4,
    ]);

    const posArr: number[] = [];
    const colArr: number[] = [];
    const rustR = 0.88, rustG = 0.52, rustB = 0.18;

    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        const dist = Math.hypot(
          nodes[i][0] - nodes[j][0],
          nodes[i][1] - nodes[j][1],
          nodes[i][2] - nodes[j][2]
        );
        if (dist < 3.5) {
          posArr.push(...nodes[i], ...nodes[j]);
          const alpha = 1 - dist / 3.5;
          colArr.push(rustR * alpha, rustG * alpha, rustB * alpha);
          colArr.push(rustR * alpha * 0.3, rustG * alpha * 0.3, rustB * alpha * 0.3);
        }
      }
    }
    return { positions: new Float32Array(posArr), colors: new Float32Array(colArr) };
  }, []);

  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    g.setAttribute("color",    new THREE.BufferAttribute(colors, 3));
    return g;
  }, [positions, colors]);

  const mat = useMemo(
    () =>
      new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.4,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      }),
    []
  );

  useFrame((_, delta) => {
    time.current += delta;
    if (!linesRef.current) return;
    linesRef.current.rotation.y = time.current * 0.06;
    linesRef.current.rotation.x = Math.sin(time.current * 0.15) * 0.1;
  });

  return <lineSegments ref={linesRef} geometry={geo} material={mat} />;
}

// Mouse-reactive camera rig
function CameraRig() {
  const { camera, size } = useThree();
  const mouse = useRef({ x: 0, y: 0 });
  const target = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handle = (e: MouseEvent) => {
      mouse.current.x = (e.clientX / size.width  - 0.5) * 2;
      mouse.current.y = (e.clientY / size.height - 0.5) * 2;
    };
    window.addEventListener("mousemove", handle);
    return () => window.removeEventListener("mousemove", handle);
  }, [size]);

  useFrame((_, delta) => {
    target.current.x += (mouse.current.x * 1.2 - target.current.x) * delta * 1.5;
    target.current.y += (-mouse.current.y * 0.8 - target.current.y) * delta * 1.5;
    camera.position.x += (target.current.x - camera.position.x) * delta * 2;
    camera.position.y += (target.current.y - camera.position.y) * delta * 2;
    camera.lookAt(0, 0, 0);
  });

  return null;
}

interface OwnershipSceneProps {
  className?: string;
}

export function OwnershipScene({ className }: OwnershipSceneProps) {
  return (
    <div className={className} aria-hidden="true">
      <Canvas
        camera={{ position: [0, 0, 7], fov: 60 }}
        gl={{
          antialias: true,
          alpha: true,
          powerPreference: "high-performance",
        }}
        style={{ background: "transparent" }}
      >
        <MemoryParticles />
        <OwnershipLines />
        <CameraRig />
      </Canvas>
    </div>
  );
}
