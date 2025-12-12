# SendFeedbackFailed

## 基本信息

- **事件显示名**: Feedback上传失败（APP评分弹窗）
- **事件英文名**: `SendFeedbackFailed`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 支付完成页 | JavaScript |  |  |  |
| `upload_failed_reason` | 上传失败原因 | STRING | 具体报错内容：具体消息内容 | JavaScript |  |  |  |
