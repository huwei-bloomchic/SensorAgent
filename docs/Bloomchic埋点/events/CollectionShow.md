# CollectionShow

## 基本信息

- **事件显示名**: 商品列表展示
- **事件英文名**: `CollectionShow`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `collection_id` | 列表ID | STRING |  | JavaScript | 商品列表展示时上报 |  |  |
| `collection_handle` | 列表handle | STRING |  | JavaScript |  |  |  |
| `is_activitylabel` | 是否开启活动标签 | BOOLEAN | app是根据全局配置的global中的product_acttag_enabled来判断 | JavaScript |  | 221117添加 |  |
| `is_functiontag` | 是否开启功能标签 | BOOLEAN | app是根据全局配置的global中的product_functag_enabled来判断 | JavaScript |  |  |  |
