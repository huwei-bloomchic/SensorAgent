# CollectionCarouselchartClick

## 基本信息

- **事件显示名**: LP轮播图模块点击<br/>LP页banner模块
- **事件英文名**: `CollectionCarouselchartClick`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `collection_id` | 列表ID | STRING |  |  |  |  |  |
| `collection_name` | 列表名称 | STRING |  |  |  |  |  |
| `pic_index` | 选中图片索引 | STRING | 有多个的话上报当前展示的轮播索引，从1开始 |  |  |  |  |
| `enabled_swiper` | 是否轮播 | STRING | 1.表示轮播， 2表示不轮播 |  |  |  |  |
| `click_url` | 跳转链接 | STRING | https::xxxxxx |  |  |  |  |
