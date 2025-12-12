# DownloadAppPopClick

## 基本信息

- **事件显示名**: web端导下载APP弹窗点击（web端）
- **事件英文名**: `DownloadAppPopClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 支付结果页 | JavaScript |  |  |  |
| `popup_type` | 3.11新增-弹窗类型 | STRING | 1. 已下载APP<br/>2.已激活<br/>3.未激活 |  |  |  |  |
| `Qr_code_link` | 二维码图片链接 | STRING |  | JavaScript |  |  |  |
| `click_type` | 点击弹窗类型 | STRING | 跳转、关闭 |  |  |  |  |
