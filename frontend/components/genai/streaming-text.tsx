"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Animates a string in chunks to simulate token streaming.
 * Use when the backend is in demo mode and there is no SSE source.
 */
export function StreamingText({
  text,
  speed = 18,
  className,
  onDone,
}: {
  text: string;
  speed?: number; // ms per token
  className?: string;
  onDone?: () => void;
}) {
  const [shown, setShown] = useState("");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    let i = 0;
    setShown("");
    const tick = () => {
      i += 1;
      setShown(text.slice(0, i));
      if (i < text.length) {
        timer.current = setTimeout(tick, speed);
      } else {
        onDone?.();
      }
    };
    tick();
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, [text, speed, onDone]);

  return (
    <span className={cn("whitespace-pre-wrap", className)}>
      {shown}
      <span
        aria-hidden
        className="ml-0.5 inline-block h-3 w-[2px] translate-y-[2px] bg-accent align-middle"
        style={{ animation: "caret-blink 1.2s ease-in-out infinite" }}
      />
    </span>
  );
}