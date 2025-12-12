# NotificationLaunch

## 基本信息

- **事件显示名**: 点击通知时上报
- **事件英文名**: `NotificationLaunch`
- **所属模块**: 客户端push
- **应埋点平台**: $url

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `string` | notification data 中的字段actionUrl |  |  |  |  |  |  |
| `string` | message.from |  |  |  |  |  |  |
| `long` | message.sentTime，单位为毫秒 |  |  |  |  |  |  |
| `string` | message.messageId |  |  |  |  |  |  |
| `int` | notification data 中的字段taskId，获取异常时上报-1 |  |  |  |  |  |  |
| `int` | notification data 中的字段taskType，<br/>0表示实时营销类push<br/>1表示场景类订单push<br/>2表示场景类物流push<br/>...<br/>获取异常时上报-1 |  |  |  |  |  |  |
