# 个人品牌视觉母题与作品集｜相关案例收录

**整理日期：2026-11-27**
**用途：** 收录本轮讨论中找到的 5 个相关案例；仅对 HAOQI.DESIGN 补充代码讲解与 Migo 可参考点。
**状态：** 案例研究资料，不代表 Migo 已选定视觉母题，也不授权直接改版或复制案例资产。

## 相关案例

### 1. HAOQI.DESIGN｜网格规则延伸到交互与转场

- [Codrops 案例文章：Inside HAOQI.DESIGN](https://tympanus.net/codrops/2026/08/15/inside-haoqi-design-letting-dom-and-webgl-share-a-retro-futurist-stage/)
- [文章转载页（用于辅助阅读代码说明）](https://thedevnews.com/inside-haoqi-design-letting-dom-and-webgl-share-a-retro-futurist-stage/)
- [HAOQI.DESIGN 网站](https://haoqi.design/)

#### 代码在做什么

案例不是把整个网页都用 WebGL 重写，而是让两种技术分工：**DOM** 负责真实网页内容和布局（标题、导航、文字、项目卡片）；**WebGL** 负责少数特殊图像效果（例如点阵揭示、图像变形或材质效果）。网页决定卡片放在哪里，画布读取其位置，再把效果准确叠加到对应区域。

| 代码／机制 | 通俗解释 | 用途 |
| --- | --- | --- |
| 滚动状态共享（文章称 `ScrollBus`） | 集中更新滚动位置，让网页与画布在同一帧读取相同状态 | 避免页面滚动时，画布效果相对卡片发生错位或延迟 |
| 指针状态共享（文章称 `PointerBus`） | 把鼠标位置统一转换成可复用的坐标，并分发给多个效果 | 让不同交互共享同一指针输入，避免重复监听、行为不一致 |
| DOM 卡片测量与画布映射 | CSS 先完成响应式布局，代码再读取卡片的位置和尺寸给 WebGL 使用 | 特效跟随真实布局，而不是用画布重做整个页面 |
| 点阵／网格揭示 | 将画面分成小单元，按一定顺序显示或切换内容 | 让网格承担“揭示、切换、进入”的动作，而非仅作背景纹理 |
| 视口与动态偏好处理 | 视口外的效果可暂停更新；减少动态效果模式下可跳过动画 | 控制性能，并兼顾偏好静态体验的用户 |

上表是对文章代码思路的概念讲解，不是逐行源码审计。原 Codrops 页面在本次读取时未能完整打开，代码说明参考公开索引和转载页；实际复用前应回到原作者当前源码核对版本和依赖。

#### 对 Migo 值得参考的内容

1. **网页结构和特殊效果分层。** 文字、导航、项目图片仍用常规 HTML/CSS，Canvas/WebGL 只处理少量确实需要的视觉效果。
2. **借鉴视觉规则，不必照搬技术复杂度。** 可先用 CSS、SVG 或图片遮罩做一个低成本点阵揭示原型；只有轻量方案无法实现且效果确有价值时，再考虑 shader/WebGL。
3. **让一种图形规则承担清楚的动作。** 点阵可以服务图片切换、内容揭示或页面进入。若只铺成背景，就还没有形成有意义的交互语言。
4. **保留作品可读性与项目自身视觉。** 效果应围绕内容出现，不要扭曲或盖住作品；Migo 的网站视觉是观看框架，不替 NED 等项目改写其 VI。
5. **动效需要性能和无障碍退路。** 控制持续渲染，触屏和键盘要有可用操作；支持 `prefers-reduced-motion`，在低性能设备上可降级或直接显示结果。

**不建议照搬：** HAOQI 的具体复古未来主义视觉、玻璃折射／色散等 Shader、整页 WebGL 化、粒子数量和转场外观。源码可见不等于其品牌图形、代码资产自动获得复用许可；复杂实现也不等于适合 Migo 当前阶段。

### 2. Good Form｜像素网格生成品牌图形

- [Marta Ryczko：Good Form](https://martaryczko.com/project/goodform)
- **案例要点：** 项目展示将像素网格用于形状、框景、图标和图像应用。值得注意的是网格作为图形生成规则，而不只是背景底纹。

### 3. Allie Orth｜用框线与网格组织作品

- [Caleb Raney：Allie Orth Portfolio](https://calebraney.webflow.io/projects/allie-orth)
- **案例要点：** 框线／网格承担内容组织功能，同时不同项目保留各自的视觉线索。可作为“网站结构统一、作品项目风格不必统一”的参考；本次未独立审计所有线上状态。

### 4. Sabato Studio｜点与圆成为交互语言

- [Communication Arts：Sabato Studio Webpick](https://www.commarts.com/webpicks/sabato-studio)
- [Communication Arts：项目页](https://www.commarts.com/project/30775/sabato-studio)
- **案例要点：** 设计说明提到点与圆延伸到粒子光标、案例色彩及页面转场。可关注点状标记如何回应操作，而不只是装饰；粒子类动效需要考虑开发和性能成本。

### 5. Adobe Illustrator｜标尺、原点与智能参考线

- [Adobe 官方帮助：标尺](https://helpx.adobe.com/illustrator/desktop/measure-and-align/grids-and-guides/about-rulers.html)
- [Adobe 官方帮助：智能参考线](https://helpx.adobe.com/illustrator/desktop/measure-and-align/grids-and-guides/about-smart-guides.html)
- **案例要点：** 这是设计工具工作流的参考，不是网页案例。标尺、原点、位置和距离提示服务于实际定位与对齐，可用于判断网站中的坐标／计数信息是否有真实语义，避免伪造软件读数作为装饰。

## 对 Migo 当前研究的简要提示

- Sommerseth 分析驱动首页 V01 仍是 Migo 当前更喜欢的整体气质参考；本组案例补充的是像素、画布、点状标记和交互机制的研究，不取代 Sommerseth。
- 目前可借鉴的是设计逻辑与实现原则，不是已经选定的母题或网站方案。
- 如果后续要验证，可先在 A 版一个局部测试静态／轻量点阵揭示，再评估它是否帮助观众理解交互；本文件本身不启动该制作。

## 查看范围说明

整理日期为 2026-11-27。HAOQI 原 Codrops 页面本次未能完整打开，代码讲解依据公开索引与转载内容作概念整理，需实施前核对原作者源码。其余案例依据公开项目说明、展示图或官方帮助文档；不代表完整源码审计、商业成效验证或所有设备实测。第三方案例只作研究，不构成对其图像、品牌资产或代码的使用授权。

[返回品牌设计案例索引](../README.md) · [视觉母题研究讨论稿 V01](../../../../01_品牌设计项目/05_品牌识别/视觉母题研究讨论稿_V01.md)