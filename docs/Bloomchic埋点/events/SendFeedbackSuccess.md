# SendFeedbackSuccess

## 基本信息

- **事件显示名**: Feedback上传成功（APP评分弹窗）
- **事件英文名**: `SendFeedbackSuccess`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `app_overall_rating` | 综合评分 | INT | 0(没有填写时报0)<br/>1、2、3、4、5 | JavaScript |  |  |  |
| `page_code` | 页面位置 | STRING | 支付完成页 | JavaScript |  |  |  |
| `Feedback_content` | Feedback内容 | STRING | 用户输入的具体内容 | JavaScript |  |  |  |
