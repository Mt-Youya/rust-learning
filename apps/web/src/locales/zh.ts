export type Translations = {
  nav: {
    curriculum: string;
    chapter1: string;
    compare: string;
    startLearning: string;
    openMenu: string;
    closeMenu: string;
    home: string;
  };
  footer: {
    tagline: string;
    builtWith: string;
  };
  theme: {
    toggleDark: string;
    toggleLight: string;
  };
  lang: {
    switchTo: string;
  };
};

export const zh: Translations = {
  nav: {
    curriculum: "课程",
    chapter1: "第一章",
    compare: "对比",
    startLearning: "开始学习",
    openMenu: "打开菜单",
    closeMenu: "关闭菜单",
    home: "RustForge 首页",
  },
  footer: {
    tagline: "为前端工程师打造 · 开源免费",
    builtWith: "Built with Rust + Next.js",
  },
  theme: {
    toggleDark: "切换到深色",
    toggleLight: "切换到浅色",
  },
  lang: {
    switchTo: "Switch to English",
  },
};
