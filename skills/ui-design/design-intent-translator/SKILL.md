---
name: design-intent-translator
description: Use when a user wants to design or revise a frontend or UI but cannot express the desired look, feel, layout, hierarchy, interaction, or visual direction in professional design language, including vague reactions, reference images, aesthetic preferences, and requests for a UI brief.
---

# Design Intent Translator

帮助用户把模糊感受变成可判断、可比较、可交付的界面方向。专业词汇是连接用户意图、视觉参考与实现约束的中间语言，不是输出目标。

## 核心原则

- 先理解产品与页面任务，再谈视觉风格。至少识别页面用途、核心用户、首要动作、内容密度和已有约束。
- 不把“高级、简洁、有科技感、不要像后台”等形容词机械映射成单一风格标签。推断它背后的层级、密度、节奏、品牌气质或交互诉求，并说明推断。
- 不维护或套用固定的术语清单。按当前问题选择准确、足够的专业表达，避免术语堆砌。
- 只有会实质改变设计方向的歧义才值得提问；一次只问一个关键问题。能从上下文合理判断时直接推进。
- 区分 AI 生成的方向示意与真实上线案例，不能把前者冒充业内实践。

## 形成设计方向

当用户尚未确定方向时，给出 2–3 个有实质差异的候选方向。差异应来自信息组织、视觉层级、页面节奏或交互方式，而不只是换颜色和圆角。

每个候选方向包含：

- 英文方向名及中文释义；
- 它如何回应用户的原始表达；
- 关键布局与视觉特征；
- 主要收益与代价；
- 一句可让用户选择、组合或排除的判断提示。

如果纯文字不足以支持判断，询问用户是否需要方向示意；需要时选择成本最低且足以比较的形式，如简易线框、视觉小样或概念图。此时不要提前制作完整产品。

如果用户已明确方向，跳过发散，直接整理 Brief。

## UI Brief 输出

英文用于专业术语和可交付表述，紧随中文释义；不必把整段内容机械翻译两遍。根据任务裁剪以下结构，不强行填满：

```markdown
## Design Direction / 设计方向

Editorial Minimalism（编辑式极简）
用中文说明该方向如何服务产品目标。

## Product Intent / 产品意图
## Information Hierarchy / 信息层级
## Layout & Density / 布局与密度
## Visual Language / 视觉语言
## Typography / 字体与排版
## Components & States / 组件与状态
## Interaction & Motion / 交互与动效
## Responsive Behavior / 响应式行为
## Accessibility / 可访问性
## Avoid / 应避免
```

Brief 应写成设计师和前端可以执行的约束。例如使用 “Typography-led hierarchy（字体主导的层级）”，并解释具体通过字号、字重和间距建立层级；不要只列风格名。

## Brief 之后

输出 UI Brief 后停止扩展，并询问：

> 是否需要我再找 1–2 个与这个方向匹配的业内优秀真实前端实现，让你直观看一下感觉？

只有用户同意后才搜索。案例具有时效性，应联网查找当前仍可访问的真实产品或高质量实现，并提供：

- 可访问链接及页面/产品名称；
- 与 Brief 对应的具体匹配点；
- 值得借鉴的结构或设计原则；
- 与用户项目不同、不宜直接照搬的部分。

不要把灵感图库里缺少产品上下文的静态图默认称为“优秀前端实现”。如果找不到足够匹配的真实案例，坦率说明，并建议改为查看概念作品或生成方向示意。

## 交接边界

除非用户同时要求实现，否则本技能止于方向、示意、Brief 与案例解释。用户确认方向并要求编码后，再把 Brief 作为约束交给合适的前端实现能力，不要在交接时稀释已经确认的设计意图。

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
