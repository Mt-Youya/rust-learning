"use client";

import { useRef, useState } from "react";
import { Play, Pause, Volume2, VolumeX, Maximize2, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { useLanguage } from "@/contexts/LanguageContext";

interface VideoPlaceholderProps {
  title: string;
  duration?: string;
  description?: string;
  youtubeId?: string;
  /** 本地视频路径，相对于 /public */
  src?: string;
  /** VTT 字幕文件路径，相对于 /public */
  subtitles?: string;
}

/** 全功能本地视频播放器，支持 VTT 字幕 */
function LocalVideoPlayer({
  src,
  title,
  duration,
  description,
  subtitles,
}: {
  src: string;
  title: string;
  duration?: string;
  description?: string;
  subtitles?: string;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [totalTime, setTotalTime] = useState(0);
  const [showControls, setShowControls] = useState(true);
  const controlsTimer = useRef<ReturnType<typeof setTimeout>>(null);

  const fmt = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${String(sec).padStart(2, "0")}`;
  };

  const togglePlay = () => {
    const v = videoRef.current;
    if (!v) return;
    if (v.paused) { v.play(); setPlaying(true); }
    else          { v.pause(); setPlaying(false); }
  };

  const toggleMute = () => {
    const v = videoRef.current;
    if (!v) return;
    v.muted = !v.muted;
    setMuted(v.muted);
  };

  const fullscreen = () => videoRef.current?.requestFullscreen?.();

  const onTimeUpdate = () => {
    const v = videoRef.current;
    if (!v) return;
    setCurrentTime(v.currentTime);
    setProgress(v.duration ? v.currentTime / v.duration : 0);
  };

  const onLoadedMetadata = () => {
    if (videoRef.current) setTotalTime(videoRef.current.duration);
  };

  const seek = (e: React.MouseEvent<HTMLDivElement>) => {
    const v = videoRef.current;
    if (!v) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    v.currentTime = ratio * v.duration;
  };

  const bumpControls = () => {
    setShowControls(true);
    if (controlsTimer.current) clearTimeout(controlsTimer.current);
    controlsTimer.current = setTimeout(() => {
      if (playing) setShowControls(false);
    }, 3000);
  };

  return (
    <div className="not-prose my-8 rounded-xl overflow-hidden border border-[oklch(0.20_0.018_265)] bg-[oklch(0.09_0.01_265)] group/player">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[oklch(0.13_0.012_265)] border-b border-[oklch(0.20_0.018_265)]">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.52_0.22_22_/_0.7)]" />
            <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.76_0.16_76_/_0.7)]" />
            <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.64_0.17_148_/_0.7)]" />
          </div>
          <span className="text-xs font-mono text-[oklch(0.60_0.02_265)] truncate max-w-[420px]">
            {title}
          </span>
        </div>
        {duration && (
          <span className="flex items-center gap-1.5 text-xs text-[oklch(0.46_0.02_265)] shrink-0">
            <Clock className="w-3 h-3" />
            {duration}
          </span>
        )}
      </div>

      {/* 视频区 */}
      <div
        className="relative aspect-video cursor-pointer select-none"
        onMouseMove={bumpControls}
        onClick={togglePlay}
      >
        <video
          ref={videoRef}
          className="w-full h-full object-contain bg-black"
          preload="metadata"
          onTimeUpdate={onTimeUpdate}
          onLoadedMetadata={onLoadedMetadata}
          onEnded={() => setPlaying(false)}
          playsInline
        >
          <source src={src} type="video/mp4" />
          {subtitles && (
            <track kind="subtitles" src={subtitles} srcLang="zh" label="中文/Subtitles" default />
          )}
        </video>

        {/* 大播放按钮（未播放时显示） */}
        {!playing && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="w-16 h-16 rounded-full bg-[oklch(0.68_0.18_42_/_0.85)] flex items-center justify-center shadow-[0_0_32px_oklch(0.68_0.18_42_/_0.4)] transition-transform duration-200 group-hover/player:scale-110">
              <Play className="w-7 h-7 text-[oklch(0.09_0.01_265)] ml-1" />
            </div>
          </div>
        )}

        {/* 底部控制栏 */}
        <div
          className={cn(
            "absolute bottom-0 left-0 right-0 transition-opacity duration-300",
            showControls || !playing ? "opacity-100" : "opacity-0"
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {/* 进度条 */}
          <div
            className="h-1.5 bg-[oklch(0.25_0.02_265)] cursor-pointer group/bar mx-0"
            onClick={seek}
          >
            <div
              className="h-full bg-[oklch(0.68_0.18_42)] relative transition-all"
              style={{ width: `${progress * 100}%` }}
            >
              <div className="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-[oklch(0.74_0.20_48)] opacity-0 group-hover/bar:opacity-100 transition-opacity" />
            </div>
          </div>

          {/* 控制按钮行 */}
          <div className="flex items-center gap-3 px-4 py-2 bg-gradient-to-t from-[oklch(0.09_0.01_265_/_0.9)] to-transparent">
            <button
              onClick={togglePlay}
              className="text-[oklch(0.82_0.01_265)] hover:text-[oklch(0.68_0.18_42)] transition-colors"
            >
              {playing
                ? <Pause className="w-5 h-5" />
                : <Play className="w-5 h-5 ml-0.5" />}
            </button>

            <button
              onClick={toggleMute}
              className="text-[oklch(0.60_0.02_265)] hover:text-[oklch(0.82_0.01_265)] transition-colors"
            >
              {muted
                ? <VolumeX className="w-4 h-4" />
                : <Volume2 className="w-4 h-4" />}
            </button>

            <span className="text-[11px] font-mono text-[oklch(0.52_0.02_265)] tabular-nums ml-1">
              {fmt(currentTime)} / {fmt(totalTime)}
            </span>

            <div className="flex-1" />

            {subtitles && (
              <span className="text-[10px] font-mono text-[oklch(0.68_0.18_42)] px-1.5 py-0.5 rounded border border-[oklch(0.68_0.18_42_/_0.4)] bg-[oklch(0.68_0.18_42_/_0.08)]">
                CC
              </span>
            )}

            <button
              onClick={fullscreen}
              className="text-[oklch(0.60_0.02_265)] hover:text-[oklch(0.82_0.01_265)] transition-colors"
            >
              <Maximize2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {description && (
        <div className="px-4 py-2 text-xs text-[oklch(0.46_0.02_265)] border-t border-[oklch(0.16_0.015_265)]">
          {description}
        </div>
      )}
    </div>
  );
}

/** YouTube embed */
function YouTubePlayer({ youtubeId, title }: { youtubeId: string; title: string }) {
  return (
    <div className="not-prose my-8 rounded-xl overflow-hidden border border-[oklch(0.20_0.018_265)]">
      <iframe
        src={`https://www.youtube.com/embed/${youtubeId}`}
        title={title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        className="w-full aspect-video"
      />
    </div>
  );
}

/** Coming-soon placeholder */
function ComingSoonPlaceholder({
  title,
  duration,
  description,
}: {
  title: string;
  duration?: string;
  description?: string;
}) {
  const { lang } = useLanguage();
  const comingSoonLabel = lang === "en" ? "VIDEO COMING SOON" : "视频即将上线";
  return (
    <div className="not-prose my-8 aspect-video max-w-3xl rounded-xl border border-[oklch(0.20_0.018_265)] bg-[oklch(0.11_0.012_265)] flex items-center justify-center relative overflow-hidden">
      <div
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: "radial-gradient(circle, oklch(0.28 0.02 265 / 0.6) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
        }}
      />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: "radial-gradient(ellipse 60% 50% at 50% 50%, oklch(0.68 0.18 42 / 0.04) 0%, transparent 70%)" }}
      />
      <div className="relative text-center space-y-4 p-8">
        <div className="w-16 h-16 mx-auto rounded-full border-2 border-[oklch(0.68_0.18_42_/_0.35)] bg-[oklch(0.68_0.18_42_/_0.08)] flex items-center justify-center">
          <Play className="w-6 h-6 text-[oklch(0.68_0.18_42)] ml-0.5" />
        </div>
        <div className="space-y-1.5">
          <p className="text-sm font-semibold text-[oklch(0.82_0.01_265)] font-display">{title}</p>
          {duration && (
            <p className="flex items-center justify-center gap-1.5 text-xs text-[oklch(0.46_0.02_265)]">
              <Clock className="w-3 h-3" />
              {duration}
            </p>
          )}
          {description && (
            <p className="text-xs text-[oklch(0.40_0.02_265)] mt-2 max-w-sm mx-auto leading-relaxed">{description}</p>
          )}
          <p className="text-[10px] font-mono text-[oklch(0.35_0.02_265)] mt-3 tracking-wide uppercase">
            {comingSoonLabel}
          </p>
        </div>
      </div>
    </div>
  );
}

/** 统一入口 */
export function VideoPlaceholder({
  title,
  duration,
  description,
  youtubeId,
  src,
  subtitles,
}: VideoPlaceholderProps) {
  if (youtubeId) return <YouTubePlayer youtubeId={youtubeId} title={title} />;
  if (src) return (
    <LocalVideoPlayer
      src={src}
      title={title}
      duration={duration}
      description={description}
      subtitles={subtitles}
    />
  );
  return <ComingSoonPlaceholder title={title} duration={duration} description={description} />;
}
