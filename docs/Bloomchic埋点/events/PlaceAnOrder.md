# PlaceAnOrder

## 基本信息

- **事件显示名**: 点击Pay now
- **事件英文名**: `PlaceAnOrder`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `currency` | 币种类型 | STRING |  | JavaScript | 点击Pay now 按钮时上报 |  | Checkout 升级<br/>PayPal暂不捕获收集不了<br/>测试工具:tiktok-pixel-helper |
| `value` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
| `content_id` | 组合后的ID | STRING |  | JavaScript |  |  |  |
| `content_type` | 固定填写:product | STRING |  | JavaScript |  |  |  |
| `content_name` | 名称 | STRING |  | JavaScript |  |  |  |
| `price` | 单件价格 | NUMBER |  | JavaScript |  |  |  |
| `quantity` | 数量 | NUMBER |  | JavaScript |  |  |  |
