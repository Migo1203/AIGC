# 目录与上传说明

更新：2026-11-08。用户指定在AIGC的`作品项目`下新建，故采用`作品项目/可调节哑铃/`，避免在仓库顶层再建孤立英文项目。现有57份资料保留原相对目录，不执行重命名或迁移原件。

## 实际创建的目录

```text
作品项目/可调节哑铃/
├─ README.md
├─ PROJECT_BRIEF.md
├─ 00_Project_Admin/
│  ├─ Asset_Inventory.csv
│  ├─ Repository_Check.md
│  ├─ Directory_and_Upload_Plan.md
│  ├─ Project_Changelog.md
│  └─ Open_Questions.md
├─ 原始资料/
│  ├─ 01 分析/       原名；含PSD，不先判断为纯研究
│  ├─ 02 Listing/    原名
│  ├─ 03 A+/         原名
│  ├─ 04 素材/       原名，来源混合待辨识
│  ├─ 05 导出/       原名，采用状态待核对
│  ├─ 亚马逊可调节哑铃产品研究项目.pdf
│  └─ 可调哑铃竞品分层分析表.xlsx
└─ 06_Optimization/
   └─ Optimization_Plan/Optimization_Roadmap.md
```

将原件副本统一保存在原始资料，避免把工作PSD、竞品参考和不明来源图片直接转为“官方参考”或“最终导出”。后续在Inventory建立关系，而不是依靠改文件名消除歧义。

## 有实际产出时再新增（本轮不铺空目录）

| 建议目录 | 创建时机及用途 |
| --- | --- |
| `01_Product_Research/` | 完整分析后保存核对后的本品事实、竞品与评论研究、来源引用；引用原PDF／Excel，不搬原件 |
| `02_Official_References/` | 已核实为本品官方资料并有来源时再建；研究可引用不代表取得商用权 |
| `03_Design_Working/V01/` | 用户授权优化后另存工作版本，按主图／次图／A+／源稿分；不覆盖历史原件 |
| `04_Design_Exports/V01/` | 保存与对应新源稿同版的实际导出及必要端／状态 |
| `05_Project_Documents/` | 有新方案PDF、Excel及说明时再建，现有原文档继续留原始资料 |
| `06_Optimization/Design_Audit/` | 用户确认资料齐全后，形成实际逐图审查报告 |
| `06_Optimization/Version_Comparisons/` | 真正产生优化前后版本后建立对照，不以改名冒充新版本 |
| `99_Archive/` | 有明确归档需要且用户同意后再使用，不批量搬走现有文件 |

新补充资料可先上传到`补充资料/批次日期/`并保留原文件名；逐批登记来源、用途和文件身份，明确之前文件是否被替代。与已存同路径同名但内容不同的文件不直接覆盖：另建批次目录保留两个版本。网页上传行为本身会产生提交，由用户自行操作或另行授权AI执行。

## 本批上传方式

截至2026-11-08直接核对GitHub官方文档：网页每文件上限25 MiB；大于25 MiB且不超过100 MiB可通过Git命令行上传；普通Git文件超过100 MiB会被拒绝；大于50 MiB有警告。MiB=1,048,576字节，注意不要与十进制MB混淆。

| 本批文件 | 精确大小 | 建议／实际方式 |
| --- | --- | --- |
| `原始资料/02 Listing/P07.psd` | 29,917,633字节（28.53 MiB） | 超过网页上限，使用Git命令行 |
| 本批其余56份文件 | 各自不超过25 MiB，精确值见Inventory | 可网页上传；本批为统一校验，全部使用Git命令行 |

本批没有超过100 MiB文件，因此不需要为本次上传启用LFS。Git LFS已安装，但本轮不新增LFS规则、不迁移旧历史。未来较大PSD／PSB／AI／视频可选择Git LFS；启用前核对账号计划、存储与下载用量及费用。LFS仓库保存指针，读取还需实际对象，不能把指针当成可读源文件。

另一选择是大源文件放Release或有权限的外部存储，在本项目登记链接、哈希、版本和访问方式，并在仓库保留可审阅预览。ZIP不会自动解决大小限制，并使逐文件查看更困难，不作为默认上传方案。

## 建议继续补充什么

先确认目标品牌／SKU、销售单位、Amazon站点和当前采用版本；补充来源链接或带来源记录的规格／实拍、现有主图与次图顺序、全部A+模块与预览、设计源稿和依赖说明、评论原样本与竞品ASIN／采集日期。现有可读文件不重复索要；PDF／Excel内部是否已有这些信息，完整分析后再列真正缺失项。

PSD／AI可原样保存，但是否能够解层与编辑需实际验证。若预览缺失，用户可从原软件另导出同版PNG／JPG／PDF并说明画板与图层；这是替代审阅方式，不冒称能够直接编辑原软件文件。本轮未改变或重新导出任何设计文件。

## 官方来源与查询日期

- 2026-11-08：[Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)，网页25 MiB与命令行100 MiB说明。
- 2026-11-08：[About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)，50 MiB警告、100 MiB限制与仓库体积建议。
- 2026-11-08：[About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)，LFS对象与套餐相关限制；未查询用户账号配额或账单。
