# ProductPageLeave

## 基本信息

- **事件显示名**: 离开商品详情页，<br/>每次离开都要上报
- **事件英文名**: `ProductPageLeave`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript | 离开商品详情页时上报，包括离开页面、关闭网页等 |  |  |
| `product_name` | 商品名称 | STRING |  | JavaScript |  |  |  |
| `is_available` | 可用状态 | BOOL |  | JavaScript |  |  |  |
| `product_handle` | 商品Handle | STRING |  |  |  |  |  |
| `last_visible_module` | 最后可见的模块 | STRING | APP特有 3.15新增 |  |  |  |  |
| `reason` | 离开的原因：返回，跳转，其他 | STRING | APP特有 3.15新增 |  |  |  |  |
| `stay_time` | 停留时长 | NUMBER | 离开时间-进入时间，单位毫秒ms | JavaScript |  |  |  |
