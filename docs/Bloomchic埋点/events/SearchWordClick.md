# SearchWordClick

## 基本信息

- **事件显示名**: 搜索联想词点击/用户点击搜索按钮/搜索历史/搜索热词<br/>搜索<br/>搜索联想<br/>搜索历史<br/>搜索热词
- **事件英文名**: `SearchWordClick`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `search_content` | 搜索关键词 | STRING |  |  |  |  |  |
| `current_module` | 当前模块：搜索；搜索联想；搜索历史；搜索热词 | STRING |  |  |  |  |  |
| `input_keyword` | 用户输入的关键词：有就上报 没有上报“” | STRING |  |  |  |  |  |
| `link` | 跳转的链接/搜索页上报“” | STRING |  |  |  |  |  |
| `media_url` | 图片地址：有就上报 没有上报“” | STRING |  |  |  |  |  |
| `module_position` | search_result 搜索结果页 | predictive_search 搜索联想 web<br/>用于区分模块展示的位置 | STRING |  |  |  |  |  |
