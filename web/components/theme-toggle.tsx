"use client";

/**
 * Switches between light and dark and remembers the choice in
 * localStorage. Without JavaScript the button never renders its handler's
 * effect and the system preference simply applies, so the site's no-JS
 * promise holds. The label is state-independent to keep server and client
 * markup identical.
 */
export function ThemeToggle({ label }: { label: string }) {
  function toggle() {
    const root = document.documentElement;
    const dark =
      root.dataset.theme === "dark" ||
      (!root.dataset.theme &&
        window.matchMedia("(prefers-color-scheme: dark)").matches);
    const next = dark ? "light" : "dark";
    root.dataset.theme = next;
    try {
      window.localStorage.setItem("theme", next);
    } catch {
      // Private browsing without storage: the choice lasts the page view.
    }
  }
  return (
    <button
      type="button"
      onClick={toggle}
      className="text-sm text-ink-secondary hover:text-ink"
    >
      {label}
    </button>
  );
}
