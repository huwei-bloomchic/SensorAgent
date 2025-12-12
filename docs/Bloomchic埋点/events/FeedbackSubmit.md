# FeedbackSubmit

## 基本信息

- **事件显示名**: Feedback提交按钮
- **事件英文名**: `FeedbackSubmit`
- **所属模块**: 6.【me页】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `email` | 登录用户email | STRING |  |  |  |  |  |
| `feedback_result` | feedback保存结果 | INT | 1是成功，0是失败 |  |  |  |  |
| `submit_failed_reason` | 提交失败原因 | STRING | review_result为0上报具体内容，为1时上报空 |  |  |  |  |
