# CollectionLeave

## 基本信息

- **事件显示名**: 离开商品列表
- **事件英文名**: `CollectionLeave`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `collection_id` | 列表ID | STRING |  | JavaScript | 离开商品列表时上报，包括离开页面、关闭网页等 |  |  |
| `collection_name` | 列表名称 | STRING |  | JavaScript |  |  |  |
| `product_number` | 当前已展示商品数 | NUMBER | 离开商品列表时，当前已浏览的商品数 | JavaScript |  |  |  |
| `stay_time` | 停留时长 | NUMBER | 离开时间-进入时间，单位毫秒ms | JavaScript |  |  |  |
