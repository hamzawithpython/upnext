export function FeedSkeleton() {
  return (
    <div className="flex flex-col gap-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="glass animate-pulse rounded-2xl p-6">
          <div className="flex gap-3">
            <div className="h-3 w-16 rounded bg-border" />
            <div className="h-3 w-12 rounded bg-border" />
          </div>
          <div className="mt-4 h-5 w-3/4 rounded bg-border" />
          <div className="mt-3 h-3 w-full rounded bg-border" />
          <div className="mt-2 h-3 w-5/6 rounded bg-border" />
          <div className="mt-4 h-16 w-full rounded-xl bg-border" />
        </div>
      ))}
    </div>
  );
}
