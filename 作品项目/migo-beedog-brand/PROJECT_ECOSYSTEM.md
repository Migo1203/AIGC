# Migo Personal Brand Ecosystem｜总项目架构

更新日期：2026-11-08。本文件记录用户确定的总项目与子项目边界；品牌定义仍以[品牌架构](01_Strategy/Brand_Architecture.md)和[品牌定位](01_Strategy/Brand_Positioning.md)为准。

## 总项目与两个子项目

Migo Personal Brand Ecosystem 是统一的个人品牌总项目，下设两个独立管理的项目。它们共享品牌一致性要求，但不合并成一个代码仓库。

| 项目 | 名称与位置 | 主要职责 |
| --- | --- | --- |
| Project A | Migo × Beedog Brand Identity；目前位于 [AIGC 仓库](https://github.com/Migo1203/AIGC)的 作品项目/migo-beedog-brand 目录 | 品牌策略、定位、命名和故事；Migo Logo；Beedog 原创角色、三视图、表情及动作；色彩、字体、辅助图形、视觉识别、品牌手册和设计源文件 |
| Project B | Migo Personal Portfolio Website；用户指定仓库名为 migo-portfolio，仓库链接 [待确认] | 网站策略与信息架构、Sitemap、Wireframe、UI 视觉、Astro / TypeScript / Tailwind CSS 开发、中英文内容、响应式页面、交互、SEO、性能、部署与维护 |

**实际仓库状态：** Project A 是 AIGC 仓库中的独立项目目录，不是当前已经单独存在的品牌专用仓库；AIGC 还包含其他作品项目。本次检查中，当前 GitHub 连接未列出 migo-portfolio，对 Migo1203/migo-portfolio 的查询返回 404；这不能证明其他账户下的同名仓库不存在。网站仓库的所属账户、实际地址及可访问性 [待确认]。本轮不创建仓库、不移动现有项目。

## 职责与权威来源

1. **品牌策略与设计的来源是 Project A。** Migo 是设计师与品牌主体，Beedog 是 Migo 的原创品牌角色；网站不重新定义两者关系。
2. Project A 负责品牌设计源文件、决策、规范和已经确认的资产导出；Project B 负责网站本身的规划、设计、实现与维护。
3. Project B 可以独立开展信息架构、内容结构和技术准备；实际品牌视觉使用以 Project A 中已确认的相应资产和规范为依据。未确认部分必须明确标为 [待确认]。
4. 网站所需的尺寸转换或技术优化应保持已确认的视觉含义和适用规则；对品牌定义、标识、角色原型或色彩规范的设计变更回到 Project A 处理。
5. Project B 使用独立副本或构建产物，不反向覆盖 Project A 的设计源文件。两个项目可分别迭代，并记录资产版本与使用位置。

## 资产流转

Project A 创作与确认 → 在[品牌资产清单](BRAND_ASSET_MANIFEST.md)登记状态、来源版本和使用条件 → 导出适用于网站的文件 → Project B 按[网站品牌接入规范](WEBSITE_BRAND_INTEGRATION.md)集成 → 如需设计变化，在 Project A 更新并重新交付。

确认以实际决策和记录为依据，不将文件存在、上传或网站引用自动视为已确认。两条工作线的阶段与依赖见[总项目路线图](PROJECT_ROADMAP.md)。

## 本轮边界

只调整项目管理文档，不修改现有设计成果，不开发网站，也不创建第三个 GitHub 仓库。网站仓库是否存在、其具体状态和实际内容均不得在未核实时假设。
