# Bloomchic埋点文档

本目录包含Bloomchic商城的埋点文档，所有埋点事件已按模块整理。

## 文档结构

- [公共属性.md](公共属性.md) - 所有事件的公共属性
- [预置属性 .md](预置属性%20.md) - 神策SDK预置属性
- [用户表.md](用户表.md) - 用户属性表
- [events/](events/) - 共271个埋点事件文件

## 埋点事件列表

共 **271** 个埋点事件文件

### 0.全局埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 挂件点击 | `ActivityPendantClick` | Web | [查看详情](events/ActivityPendantClick.md) |
| 活动挂件展示 | `ActivityPendantShow` | Web | [查看详情](events/ActivityPendantShow.md) |
| 点击加入心愿单 | `AddToWishlist` | Android,Web,IOS | [查看详情](events/AddToWishlist.md) |
| 点击BloomChic | `BloomChicClick` | Web | [查看详情](events/BloomChicClick.md) |
| 点击在线客服按钮 | `ChatClick` | Web | [查看详情](events/ChatClick.md) |
| 隐私协议，用户是否允许数据收集 | `CustomizeCookiesResult` | Android,IOS | [查看详情](events/CustomizeCookiesResult.md) |
| Http响应失败 | `HttpResponseError` | Android,IOS | [查看详情](events/HttpResponseError.md) |
| 登录注册成功 | `LoginRegisterResult` | 服务端 | [查看详情](events/LoginRegisterResult.md) |
| 点击导航栏具体栏目 | `NavigationBarClick` | Web | [查看详情](events/NavigationBarClick.md) |
| 导航栏展示/隐藏 | `NavigationBarShow_NavigationBarHide` | Web | [查看详情](events/NavigationBarShow_NavigationBarHide.md) |
| 数据加载结果 | `PageDataLoadResult` | Android,IOS | [查看详情](events/PageDataLoadResult.md) |
| 上划页面 | `PageSwipeUp` | Web | [查看详情](events/PageSwipeUp.md) |
| 密码重置/忘记密码提交点击 | `PasswordResetClick` | Android,Web,IOS | [查看详情](events/PasswordResetClick.md) |
| 密码重置/忘记密码页展示 | `PasswordResetPageShow` | Android,Web,IOS | [查看详情](events/PasswordResetPageShow.md) |
| 密码重置/忘记密码失败（失败才上报） | `PasswordResetResult` | Android,Web,IOS | [查看详情](events/PasswordResetResult.md) |
| 活动倒计时点击 （首页、商详页） | `ProductCountdownClick` | Web | [查看详情](events/ProductCountdownClick.md) |
| 活动倒计时展示 （首页、商详页） | `ProductCountdownShow` | Web | [查看详情](events/ProductCountdownShow.md) |
| 记录web性能 | `RecordWebPerformance` | Web | [查看详情](events/RecordWebPerformance.md) |
| 注册提交点击 | `RegisterClick` | Android,Web,IOS | [查看详情](events/RegisterClick.md) |
| 注册提交失败（失败才上报） | `RegisterClickResult` | Android,Web,IOS | [查看详情](events/RegisterClickResult.md) |
| 注册页展示 | `RegisterPageShow` | Android,Web,IOS | [查看详情](events/RegisterPageShow.md) |
| 点击加入心愿单 | `RemoveFromWishlist` | Android,Web,IOS | [查看详情](events/RemoveFromWishlist.md) |
| 点击搜索按钮 | `SearchButtonClick` | Web | [查看详情](events/SearchButtonClick.md) |
| 搜索请求失败 | `SearchFailed` | Android,Web,IOS | [查看详情](events/SearchFailed.md) |
| 搜索联想面板展示隐藏 | `SearchPredictivePanel` | Web | [查看详情](events/SearchPredictivePanel.md) |
| SearchResult 返回搜索结果时上报 有搜索到内容就上报true，否则是false， 有筛选条件时不上报，同fb上报逻辑， 异常时不上报 | `SearchResult` | Android,Web,IOS | [查看详情](events/SearchResult.md) |
| 搜索联想词点击/用户点击搜索按钮/搜索历史/搜索热词 搜索 搜索联想 搜索历史 搜索热词 | `SearchWordClick` | Android,IOS | [查看详情](events/SearchWordClick.md) |
| 点击购物车按钮 | `ShoppingCartClick` | Web | [查看详情](events/ShoppingCartClick.md) |
| 登录提交点击 | `SignInClick` | Android,Web,IOS | [查看详情](events/SignInClick.md) |
| 登录结果失败失败（失败才上报） | `SignInClickResult` | ## 事件属性 | [查看详情](events/SignInClickResult.md) |
| 登录页展示 | `SignInPageShow` | Android,Web,IOS | [查看详情](events/SignInPageShow.md) |
| URL重定向 | `WebviewOverrideUrl` | Android,IOS | [查看详情](events/WebviewOverrideUrl.md) |

### 0.APP特有的埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| APP启屏页点击 | `APPLaunchPageClick` | Android,IOS | [查看详情](events/APPLaunchPageClick.md) |
| APP启屏页关闭 | `APPLaunchPageClose` | Android,IOS | [查看详情](events/APPLaunchPageClose.md) |
| APP启屏页展示 | `APPLaunchPageShow` | Android,IOS | [查看详情](events/APPLaunchPageShow.md) |
| APP启动时上报 | `AppLaunch` | Android,IOS | [查看详情](events/AppLaunch.md) |
| 点击push通知消息后上报 Push消息被点击 | `PushNotificationMessageClick` | Android,IOS | [查看详情](events/PushNotificationMessageClick.md) |
| 站点切换操作 | `SwitchSite` | Android,IOS | [查看详情](events/SwitchSite.md) |
| 站点切换弹窗点击 | `SwitchSitePageClick` | Android,IOS | [查看详情](events/SwitchSitePageClick.md) |
| 切换站点弹窗展示 | `SwitchSitePageShow` | Android,IOS | [查看详情](events/SwitchSitePageShow.md) |
| AppsFlyer 回调deeplink成功的 时候上报 | `af_deeplink_launch` | Android,IOS | [查看详情](events/af_deeplink_launch.md) |
| AppsFlyer 回调onConversionDataSuccess， is_first_launch = true 时候上报 AF归因成功首次启动 Android 2.10/iOS 2.8版本新增 | `af_first_launch` | Android,IOS | [查看详情](events/af_first_launch.md) |

### 1.【首页】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| web首页底部订阅 | `BottomSubscription` | Web | [查看详情](events/BottomSubscription.md) |
| 点击关闭按钮 | `CloseButtonClick` | Web | [查看详情](events/CloseButtonClick.md) |
| 关闭确认弹窗点击 | `CloseConfirmClick` | Web | [查看详情](events/CloseConfirmClick.md) |
| 关闭确认弹窗展示 | `CloseConfirmShow` | Web | [查看详情](events/CloseConfirmShow.md) |
| 点击抽奖结果页 | `ContinueShoppingClick` | Web | [查看详情](events/ContinueShoppingClick.md) |
| 转盘前置弹窗点击按钮 | `CouponPopupButtonClick` | Web | [查看详情](events/CouponPopupButtonClick.md) |
| 转盘前置弹窗点击关闭 | `CouponPopupCloseClick` | Web | [查看详情](events/CouponPopupCloseClick.md) |
| 转盘前置弹窗展示 | `CouponPopupShow` | Web | [查看详情](events/CouponPopupShow.md) |
| 离开首页 | `FrontPageLeave` | Web | [查看详情](events/FrontPageLeave.md) |
| 首页展示 | `FrontPageShow` | Web | [查看详情](events/FrontPageShow.md) |
| 首页弹窗点击 | `HomeActivityClick` | Android,Web,IOS | [查看详情](events/HomeActivityClick.md) |
| 首页弹窗展示 | `HomeActivityShow` | Android,Web,IOS | [查看详情](events/HomeActivityShow.md) |
| 点击资源位 （含全站资源位） | `ResourceClick` | Web | [查看详情](events/ResourceClick.md) |
| 资源位展示 （含全站资源位） | `ResourceShow` | Android,Web,IOS | [查看详情](events/ResourceShow.md) |
| 点击规则条款 | `RulesClick` | Web | [查看详情](events/RulesClick.md) |
| footer点击订阅 | `SMSsubscribe` | Web | [查看详情](events/SMSsubscribe.md) |
| 点击转盘功能入口 | `SpinEntryClick` | Web | [查看详情](events/SpinEntryClick.md) |
| 转盘功能入口点击关闭 | `SpinEntryCloseClick` | Web | [查看详情](events/SpinEntryCloseClick.md) |
| 转盘功能入口展示 | `SpinEntryShow` | Web | [查看详情](events/SpinEntryShow.md) |
| 转盘弹窗页面展示 | `SpinPopupShow` | Web | [查看详情](events/SpinPopupShow.md) |
| 抽奖结果页展示 | `SpinResultShow` | Web | [查看详情](events/SpinResultShow.md) |
| 邮箱步骤点击 | `StarSpinTheWheel` | Web | [查看详情](events/StarSpinTheWheel.md) |
| SMS步骤点击抽奖 | `StarSpinTheWheelSMS` | Web | [查看详情](events/StarSpinTheWheelSMS.md) |
| web注册成功 | `WebRegisterClick` | Web | [查看详情](events/WebRegisterClick.md) |
| - **事件英文名**: `首页抽奖大转盘——大转盘弹窗功能 —[ 2021.9.26更新 ]` | `首页抽奖大转盘大转盘弹窗功能_2021926更新_` |  | [查看详情](events/首页抽奖大转盘大转盘弹窗功能_2021926更新_.md) |

### 2.【商品】相关埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 全选我的filter | `AllSelectMyFilter` | Android,Web,IOS | [查看详情](events/AllSelectMyFilter.md) |
| LP轮播图模块点击 LP页banner模块 | `CollectionCarouselchartClick` | Web | [查看详情](events/CollectionCarouselchartClick.md) |
| LP分类tag位点击 | `CollectionCategoryTagClick` | Web | [查看详情](events/CollectionCategoryTagClick.md) |
| LP倒计时点击 | `CollectionCountdownClick` | Web | [查看详情](events/CollectionCountdownClick.md) |
| LP筛选点击 | `CollectionFilterlClick` | Web | [查看详情](events/CollectionFilterlClick.md) |
| 离开商品列表 | `CollectionLeave` | Android,Web,IOS | [查看详情](events/CollectionLeave.md) |
| LP模特图资源位点击 | `CollectionModelImagelClick` | Web | [查看详情](events/CollectionModelImagelClick.md) |
| LP模特图选项点击 | `CollectionModelSizelClick` | Web | [查看详情](events/CollectionModelSizelClick.md) |
| LP多图模块点击 | `CollectionMultigraphmoduleClick` | Web | [查看详情](events/CollectionMultigraphmoduleClick.md) |
| LP资源位展示 | `CollectionResourceShow` | Web | [查看详情](events/CollectionResourceShow.md) |
| 商品列表展示 | `CollectionShow` | Android,Web,IOS | [查看详情](events/CollectionShow.md) |
| 点击翻页 | `CollectionTurnPage` | Web | [查看详情](events/CollectionTurnPage.md) |
| 删除【我的Filter】 | `DeleteMyFilter` | Android,Web,IOS | [查看详情](events/DeleteMyFilter.md) |
| 点击filter弹窗的清除 | `FilterClearClick` | Android,Web,IOS | [查看详情](events/FilterClearClick.md) |
| 点击[Filter]icon | `FilterClick` | Android,Web,IOS | [查看详情](events/FilterClick.md) |
| 点击filter弹窗的提交 | `FilterDoneClick` | Android,Web,IOS | [查看详情](events/FilterDoneClick.md) |
| 筛选成功的筛选项 | `FilterSelect` | Android,Web,IOS | [查看详情](events/FilterSelect.md) |
| 单列双列切换按钮点击 | `ListViewModeClick` | Android,Web,IOS | [查看详情](events/ListViewModeClick.md) |
| 我的filter保存点击 | `MyFilterSaveClick` | Android,Web,IOS | [查看详情](events/MyFilterSaveClick.md) |
| 点击商品 | `ProductClick` | Android,Web,IOS | [查看详情](events/ProductClick.md) |
| 商品在列表中的展示 | `ProductShow` | Android,Web,IOS | [查看详情](events/ProductShow.md) |
| QuickView点击 | `QuickViewClick` | Web | [查看详情](events/QuickViewClick.md) |
| QuickView展示 | `QuickViewShow` | Web | [查看详情](events/QuickViewShow.md) |
| 使用某个排序 | `SortMethodClick` | Web | [查看详情](events/SortMethodClick.md) |
| 列表SKC点击 | `list_skc_click` | Android,Web,IOS | [查看详情](events/list_skc_click.md) |
| 列表SKC滑动开始 | `list_skc_slide` | Android,Web,IOS | [查看详情](events/list_skc_slide.md) |
| - **事件英文名**: `全局商品维度埋点` | `全局商品维度埋点` |  | [查看详情](events/全局商品维度埋点.md) |
| - **事件英文名**: `商品列表` | `商品列表` |  | [查看详情](events/商品列表.md) |

### 3.【商详页】的埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 收藏成功 | `AddFromWishlist` | Android,Web,IOS | [查看详情](events/AddFromWishlist.md) |
| 成功加入购物车 | `AddToCartClick` | Android,Web,IOS | [查看详情](events/AddToCartClick.md) |
| 商品详情插件搭配销售加购 | `AlsoInOurToCart` | Web | [查看详情](events/AlsoInOurToCart.md) |
| 点击查看大图 | `BigPictureClick` | Web | [查看详情](events/BigPictureClick.md) |
| 点击加入购物车（3.12版本新增） | `ClickAddCartButton` | Android,Web,IOS | [查看详情](events/ClickAddCartButton.md) |
| 点击商品详情页评论区域 | `DetailReviewClick` | Android,Web,IOS | [查看详情](events/DetailReviewClick.md) |
| Fabric & Care点击 | `FabricCareClick` | Android,Web,IOS | [查看详情](events/FabricCareClick.md) |
| 客服按钮点击 | `HelpCenterClick_删除ProductSupportClick` | Android,Web,IOS | [查看详情](events/HelpCenterClick_删除ProductSupportClick.md) |
| size页面展示 | `MySizeShow` | Android,Web,IOS | [查看详情](events/MySizeShow.md) |
| 商品AlsoInCart模块曝光 | `ProductAlsoInCartShow` | Web | [查看详情](events/ProductAlsoInCartShow.md) |
| Shipping & Returns 点击change location | `ProductChangeLocationClick` | Android,Web,IOS | [查看详情](events/ProductChangeLocationClick.md) |
| 点击收藏 | `ProductCollectClick` | Android,Web,IOS | [查看详情](events/ProductCollectClick.md) |
| 商品详情描述图片曝光 | `ProductDescriptionImageShow` | Android,Web,IOS | [查看详情](events/ProductDescriptionImageShow.md) |
| Description图文详情模块点击 | `ProductDescriptionMediaClick` | Android,Web,IOS | [查看详情](events/ProductDescriptionMediaClick.md) |
| 商详卖点展示 | `ProductDescriptionMediaExposure` | Android,Web,IOS | [查看详情](events/ProductDescriptionMediaExposure.md) |
| 商品详情资源媒体点击（点击会进入图片浏览页面，视频会播放） | `ProductMediaClick` | Android,Web,IOS | [查看详情](events/ProductMediaClick.md) |
| 商品详情资源媒体曝光 包括点击图片资源进入图片浏览页面的图片曝光 | `ProductMediaExposure` | Android,Web,IOS | [查看详情](events/ProductMediaExposure.md) |
| 点击下拉模特 | `ProductModelSizeClick` | Web | [查看详情](events/ProductModelSizeClick.md) |
| 点击下拉模特选择的选项 | `ProductModelSizeSelected` | Web | [查看详情](events/ProductModelSizeSelected.md) |
| 商品选项点击 | `ProductOptionClick` | Android,Web,IOS | [查看详情](events/ProductOptionClick.md) |
| 离开商品详情页， 每次离开都要上报 | `ProductPageLeave` | Android,Web,IOS | [查看详情](events/ProductPageLeave.md) |
| 商品加载失败 | `ProductPageLoadFailed` | IOS | [查看详情](events/ProductPageLoadFailed.md) |
| 商品详情页展示/ 微商详展示 （APP 3.9 新增） | `ProductPageShow` | Android,Web,IOS | [查看详情](events/ProductPageShow.md) |
| Shipping & Returns 点击details | `ProductReturnDetailsClick` | Android,Web,IOS | [查看详情](events/ProductReturnDetailsClick.md) |
| 商详评论模块展示（这个评论模块的展示上报） | `ProductReviewModuleShow_之前的ProductReviewShow有几条优质评论就上报几次` | Android,Web,IOS | [查看详情](events/ProductReviewModuleShow_之前的ProductReviewShow有几条优质评论就上报几次.md) |
| 商详评论展示/评论列表中 评论展示 （单条评论维度的商上报，展示1条上报1次） | `ProductReviewShow` | Android,Web,IOS | [查看详情](events/ProductReviewShow.md) |
| 分享按钮点击 | `ProductShareClick` | Android,Web,IOS | [查看详情](events/ProductShareClick.md) |
| 商品详情页快递模块曝光 | `ProductShippingShow` | Android,Web,IOS | [查看详情](events/ProductShippingShow.md) |
| 点击size guide | `ProductSizeGuideClick` | Android,Web,IOS | [查看详情](events/ProductSizeGuideClick.md) |
| 商品尺码推荐点击 | `ProductSizeRecommendationClick` | Android,Web,IOS | [查看详情](events/ProductSizeRecommendationClick.md) |
| 商品尺码接口响应 在服务端返回的need_ab_test = true才上报 | `ProductSizeRecommendationResponse` | Android,Web,IOS | [查看详情](events/ProductSizeRecommendationResponse.md) |
| 商品尺码推荐展示 | `ProductSizeRecommendationShow` | Android,Web,IOS | [查看详情](events/ProductSizeRecommendationShow.md) |
| 商详左下角客服点击 | `ProductSupportClick` | Android,Web,IOS | [查看详情](events/ProductSupportClick.md) |
| 商详页点击商品评分 | `ProductTitleStarClick` | Android,Web,IOS | [查看详情](events/ProductTitleStarClick.md) |
| 商品Variant展示（3.21版本新增） | `ProductVariantShow` | Android,Web,IOS | [查看详情](events/ProductVariantShow.md) |
| 商品视频展示 | `ProductVideoShow` | Android,Web,IOS | [查看详情](events/ProductVideoShow.md) |
| 点击一键加购 | `QuickBuyClick` | Android,Web,IOS | [查看详情](events/QuickBuyClick.md) |
| 评价列表展示 | `ReviewListShow` | Android,Web,IOS | [查看详情](events/ReviewListShow.md) |
| 点击评论块中图片/视频 | `ReviewMediaClick` | Android,Web,IOS | [查看详情](events/ReviewMediaClick.md) |
| 评论大图曝光 | `ReviewMediaShow` | Android,Web,IOS | [查看详情](events/ReviewMediaShow.md) |
| 使用某个排序方式 | `ReviewSortMethodClick` | Android,Web,IOS | [查看详情](events/ReviewSortMethodClick.md) |
| 点击SizeGuide | `SizeGuideClick` | Android,Web,IOS | [查看详情](events/SizeGuideClick.md) |
| 视频播放开始 | `VideoPlayStart` | Android,Web,IOS | [查看详情](events/VideoPlayStart.md) |
| 视频播放停止 （离开，或者播放结束时上报） | `VideoPlayStop` | Android,Web,IOS | [查看详情](events/VideoPlayStop.md) |
| 点击Add Your Review | `WriteReviewButtonClick` | Android,Web,IOS | [查看详情](events/WriteReviewButtonClick.md) |
| YouMightAlsoLike展示 | `YouMightAlsoLike` | Web | [查看详情](events/YouMightAlsoLike.md) |

### 4.【购物车】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 微商详浮层展示 | `BriefProductShow` | ## 事件属性 | [查看详情](events/BriefProductShow.md) |
| 搭配推荐Build My Outfit点击 | `BuildMyOutfitClick` | Android,Web,IOS | [查看详情](events/BuildMyOutfitClick.md) |
| 搭配推荐Build My Outfit展示 | `BuildMyOutfitShow` | Android,Web,IOS | [查看详情](events/BuildMyOutfitShow.md) |
| 点击【ADD】 | `CartAddClick` | Android,iOS | [查看详情](events/CartAddClick.md) |
| 优惠券【X】点击 | `CartCancelCoupon` | Android,iOS | [查看详情](events/CartCancelCoupon.md) |
| 点击商品的换尺码 | `CartChangeSkuClick` | Android,iOS | [查看详情](events/CartChangeSkuClick.md) |
| 券列表页点击Copy | `CartCouponCopyClick` | Android,iOS | [查看详情](events/CartCouponCopyClick.md) |
| 券包列表展示 | `CartCouponsListShow` | Android,iOS | [查看详情](events/CartCouponsListShow.md) |
| 点击【coupons】 | `CartCouponsModuleClick` | Android,iOS | [查看详情](events/CartCouponsModuleClick.md) |
| 点击购物车折扣区域 | `CartDiscountTipsClick` | Android,iOS | [查看详情](events/CartDiscountTipsClick.md) |
| 点击购物车【编辑】按钮 | `CartEditClick` | Android,iOS | [查看详情](events/CartEditClick.md) |
| 退出编辑 | `CartEditDoneClick` | Android,iOS | [查看详情](events/CartEditDoneClick.md) |
| Event Discount展示 | `CartEventDiscountShow` | Android,iOS | [查看详情](events/CartEventDiscountShow.md) |
| 点击【giftcard】 | `CartGiftCardModuleClick` | Android,iOS | [查看详情](events/CartGiftCardModuleClick.md) |
| giftcard列表展示 | `CartGiftcardListShow` | Android,iOS | [查看详情](events/CartGiftcardListShow.md) |
| 手动用券结果（手动用券，点击【apply】） | `CartHandCoupon` | Android,iOS | [查看详情](events/CartHandCoupon.md) |
| 点击商品计步器【-】 | `CartOdometerClick` | Android,iOS | [查看详情](events/CartOdometerClick.md) |
| 购物车展示 | `CartShow` | Android,iOS,M端,PC端 | [查看详情](events/CartShow.md) |
| 点击顶部signin 横幅的 | `CartSinginClick` | Android,iOS | [查看详情](events/CartSinginClick.md) |
| 点击购物【summary】 | `CartSummaryClick` | Android,iOS | [查看详情](events/CartSummaryClick.md) |
| 点击购物车顶部【收藏夹】按钮 | `CartWishlistClick` | Android,iOS | [查看详情](events/CartWishlistClick.md) |
| 点击Check Out按钮 | `CheckOutClick` | Android,Web,IOS | [查看详情](events/CheckOutClick.md) |
| 结算开始(app端特有) | `CheckOutStart` | Android,IOS | [查看详情](events/CheckOutStart.md) |
| Checkout接口请求失败 | `CheckoutCreateFailed` | Android,iOS | [查看详情](events/CheckoutCreateFailed.md) |
| 搭配浮层加购点击 | `OutfitCartClick` | ## 事件属性 | [查看详情](events/OutfitCartClick.md) |
| 搭配商品类型切换tab点击 | `OutfitTypeClick` | Android,Web,IOS | [查看详情](events/OutfitTypeClick.md) |
| 搭配浮层收藏点击 | `OutfitWishlistClick` | ## 事件属性 | [查看详情](events/OutfitWishlistClick.md) |
| 点击pre-order的【?】 | `PreOrderInstructionsClick` | Android,iOS | [查看详情](events/PreOrderInstructionsClick.md) |
| 商品进入结算 | `ProductCheckOutClick` | Android,Web,IOS | [查看详情](events/ProductCheckOutClick.md) |
| 结算开始(app端特有) | `ProductCheckOutStart` | Android,IOS | [查看详情](events/ProductCheckOutStart.md) |
| 点击【delete】 按照商品维度单个上报 | `RemoveFromCart` | Android,iOS | [查看详情](events/RemoveFromCart.md) |

### 5.【checkout到下单支付】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| APP评分弹窗展示 | `AppReviewShow` | Android,IOS | [查看详情](events/AppReviewShow.md) |
| 点击Back to cart | `BackToCartClick` | Android,Web | [查看详情](events/BackToCartClick.md) |
| 点击Change按钮 | `ChangeButtonClick` | Android,Web | [查看详情](events/ChangeButtonClick.md) |
| 支付结果，手机端专属，由于调用H5 进行结算，增加上报用来交叉验证 | `CheckoutFinish` | Android,IOS | [查看详情](events/CheckoutFinish.md) |
| 勾选订阅【Email me with news and offers】 | `CheckoutPageClick` | Android,Web,IOS | [查看详情](events/CheckoutPageClick.md) |
| 结算页展示 | `CheckoutPageShow` | Android,Web,IOS | [查看详情](events/CheckoutPageShow.md) |
| 结算页面一进入 | `CheckoutPageStart` | Android,Web,IOS | [查看详情](events/CheckoutPageStart.md) |
| 结算-券&giftcard应用 | `CheckoutRewardsApply` | Web | [查看详情](events/CheckoutRewardsApply.md) |
| 结算-兑换入口点击 | `CheckoutRewardsEntryClick` | Web | [查看详情](events/CheckoutRewardsEntryClick.md) |
| 结算-兑换入口展示 | `CheckoutRewardsEntryShow` | Web | [查看详情](events/CheckoutRewardsEntryShow.md) |
| 结算-奖品登录入口点击 | `CheckoutRewardsLogin` | Web | [查看详情](events/CheckoutRewardsLogin.md) |
| 结算-券&giftcard兑换 | `CheckoutRewardsRedeem` | Web | [查看详情](events/CheckoutRewardsRedeem.md) |
| 选择邮寄方式 【Shipping method】 | `CheckoutShippingSelect` | Android,Web,IOS | [查看详情](events/CheckoutShippingSelect.md) |
| tp入口点击事件 | `CheckoutTrustpilotClick` | Web | [查看详情](events/CheckoutTrustpilotClick.md) |
| tp入口展示 | `CheckoutTrustpilotShow` | Android,Web,IOS | [查看详情](events/CheckoutTrustpilotShow.md) |
| 应用优惠或礼品卡 | `CouponApplied` | Android,Web,IOS | [查看详情](events/CouponApplied.md) |
| web页面导下载点击（PC端） | `DownloadAppClick` | Web | [查看详情](events/DownloadAppClick.md) |
| web端导下载APP弹窗点击（web端） | `DownloadAppPopClick` | Web | [查看详情](events/DownloadAppPopClick.md) |
| web端导下载APP弹窗展示（web端） | `DownloadAppPopShow` | Web | [查看详情](events/DownloadAppPopShow.md) |
| web页面导下载展示（PC端） | `DownloadAppShow` | Web | [查看详情](events/DownloadAppShow.md) |
| 关闭按钮点击（APP评分弹窗） | `NotNowClick` | Android,IOS | [查看详情](events/NotNowClick.md) |
| 订单快捷查询模块点击 | `OrderQuickClick` | Android,IOS | [查看详情](events/OrderQuickClick.md) |
| 订单快捷查询模块关闭 | `OrderQuickClose` | Android,IOS | [查看详情](events/OrderQuickClose.md) |
| 订单快捷查询模块展示 | `OrderQuickShow` | Android,IOS | [查看详情](events/OrderQuickShow.md) |
| 点击Order summary | `OrderSummaryClick` | Web | [查看详情](events/OrderSummaryClick.md) |
| 点击Pay now | `PayNowButtonClick` | Android,Web,IOS | [查看详情](events/PayNowButtonClick.md) |
| 支付完成 | `PaymentComplete` | Android,Web | [查看详情](events/PaymentComplete.md) |
| ThankYou页,订单详情页展示 | `PaymentSuccessShow` | Android,Web,IOS | [查看详情](events/PaymentSuccessShow.md) |
| 点击Pay now | `PlaceAnOrder` | Web | [查看详情](events/PlaceAnOrder.md) |
| 支付成功详情（后端） 按单个商品上报，一次购买多个商品就上报多条 | `ProductPurchaseSuccess` | ## 事件属性 | [查看详情](events/ProductPurchaseSuccess.md) |
| 支付成功（支付（后端）（Android 2.8） | `PurchaseSuccess` | ## 事件属性 | [查看详情](events/PurchaseSuccess.md) |
| AppPush前置引导弹窗点击 | `PushPermissionPopClick` | Android,IOS | [查看详情](events/PushPermissionPopClick.md) |
| AppPush前置引导通知权限结果 | `PushPermissionPopResult` | Android,IOS | [查看详情](events/PushPermissionPopResult.md) |
| AppPush前置引导弹窗展示 | `PushPermissionPopShow` | Android,IOS | [查看详情](events/PushPermissionPopShow.md) |
| 礼品卡SendAsGift按钮点击 | `SendAsGiftClick` | Android,IOS | [查看详情](events/SendAsGiftClick.md) |
| Feedback上传失败（APP评分弹窗） | `SendFeedbackFailed` | Android,IOS | [查看详情](events/SendFeedbackFailed.md) |
| Feedback上传成功（APP评分弹窗） | `SendFeedbackSuccess` | Android,IOS | [查看详情](events/SendFeedbackSuccess.md) |
| 订单页展示用券提示弹窗点击 （订单页展示用券提示） | `UseCouponDialogClick` | Web | [查看详情](events/UseCouponDialogClick.md) |
| 订单页展示用券提示弹窗展示— （订单页展示用券提示） | `UseCouponDialogShow` | Web | [查看详情](events/UseCouponDialogShow.md) |
| 使用券结果 （订单页展示用券提示） | `UseCouponResult` | Web | [查看详情](events/UseCouponResult.md) |
| Yes按钮点击（APP评分弹窗） | `YesReviewClick` | Android,IOS | [查看详情](events/YesReviewClick.md) |
| 点击Pay now | `add_payment_info` | Web | [查看详情](events/add_payment_info.md) |
| Firebase PUSH Token | `fcm_token` | Android,IOS | [查看详情](events/fcm_token.md) |
| - **事件英文名**: `手机端通过神策埋点的打通H5的能力，由H5上报https://manual.sensorsdata.cn/sa/latest/tech_sdk_client_link-1573914.html` | `手机端通过神策埋点的打通H5的能力由H5上报httpsmanualsensorsdatacnsalatesttech_sdk_client_link_1573914html` |  | [查看详情](events/手机端通过神策埋点的打通H5的能力由H5上报httpsmanualsensorsdatacnsalatesttech_sdk_client_link_1573914html.md) |

### 6.【退货退款】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 部分仅退款 提醒 弹窗曝光 | `PartRefundRemindPopup` | ## 事件属性 | [查看详情](events/PartRefundRemindPopup.md) |
| 部分仅退款弹窗【跳过】或【下一步】按钮点击 | `PartialRefundOnlyClick` | Android,web,IOS | [查看详情](events/PartialRefundOnlyClick.md) |
| 部分仅退款弹窗曝光 | `PartialRefundOnlyPopup` | Android,web,IOS | [查看详情](events/PartialRefundOnlyPopup.md) |
| 退款成功（SKU维度） | `ProductRefundSuccess` | 服务端 | [查看详情](events/ProductRefundSuccess.md) |
| 商品退货（SKU维度） | `ProductReturn` | 服务端 | [查看详情](events/ProductReturn.md) |
| 退货成功（SKU维度） | `ProductReturnSuccess` | 服务端 | [查看详情](events/ProductReturnSuccess.md) |
| 进入退货页面 | `RefundPage` | Android,web,IOS | [查看详情](events/RefundPage.md) |
| 退货退款 预提交页面曝光 | `RefundSubmitPage` | Android,web,IOS | [查看详情](events/RefundSubmitPage.md) |
| 选择退货商品页面曝光 | `SelectRefundItemsPage` | Android,web,IOS | [查看详情](events/SelectRefundItemsPage.md) |
| 选择退货原因【下一步】按钮点击 | `SelectReturnReasonNextClick` | Android,web,IOS | [查看详情](events/SelectReturnReasonNextClick.md) |
| 选择退货原因页面曝光 | `SelectReturnReasonPage` | Android,web,IOS | [查看详情](events/SelectReturnReasonPage.md) |
| - **事件英文名**: `手机端通过神策埋点的打通H5的能力，由H5上报https://manual.sensorsdata.cn/sa/latest/tech_sdk_client_link-1573914.html` | `手机端通过神策埋点的打通H5的能力由H5上报httpsmanualsensorsdatacnsalatesttech_sdk_client_link_1573914html_6退货退款埋点_2` |  | [查看详情](events/手机端通过神策埋点的打通H5的能力由H5上报httpsmanualsensorsdatacnsalatesttech_sdk_client_link_1573914html_6退货退款埋点_2.md) |

### 6.【me页】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 地址库地址 | `AddressClick` | Android,IOS | [查看详情](events/AddressClick.md) |
| Feedback点击 | `FeedbackEntranceClick` | Android,Web,IOS | [查看详情](events/FeedbackEntranceClick.md) |
| Feedback展示 | `FeedbackEntranceShow` | Android,Web,IOS | [查看详情](events/FeedbackEntranceShow.md) |
| Feedback提交按钮 | `FeedbackSubmit` | Android,IOS | [查看详情](events/FeedbackSubmit.md) |
| 个人中心Me点击 | `MeClick` | Android,IOS | [查看详情](events/MeClick.md) |
| 个人中心Me展示 | `MeShow` | Android,IOS | [查看详情](events/MeShow.md) |
| 我的菜单项点击 | `MineMenuItemClick` | Android,iOS,M端 | [查看详情](events/MineMenuItemClick.md) |
| 我的账号点击 | `MyAccountClick` | Android,IOS | [查看详情](events/MyAccountClick.md) |
| 优惠券中心点击 | `MyCouponsClick` | Android,IOS | [查看详情](events/MyCouponsClick.md) |
| 个人中心我的菜单点击 | `MyMenuClick` | Android,IOS | [查看详情](events/MyMenuClick.md) |
| 我的订单点击 | `MyOrdersClick` | Android,IOS | [查看详情](events/MyOrdersClick.md) |
| 点击个人信息编辑按钮 | `MyProfileClick` | Android,iOS,M端 | [查看详情](events/MyProfileClick.md) |
| 我的评论点击 | `MyReviewsClick` | Android,IOS | [查看详情](events/MyReviewsClick.md) |
| 我的收藏夹点击 | `MyWishlistClick` | Android,IOS | [查看详情](events/MyWishlistClick.md) |
| 登录注册入口点击 | `SignRegisterClick` | Android,IOS | [查看详情](events/SignRegisterClick.md) |
| 点击【delivered】 | `TrackDeliveredClick` | M端 | [查看详情](events/TrackDeliveredClick.md) |
| 点击【details】 | `TrackDetailsClick` | M端 | [查看详情](events/TrackDetailsClick.md) |
| 点击【in transit】 | `TrackInTransitClick` | M端 | [查看详情](events/TrackInTransitClick.md) |
| 评论提交后上报：成功/失败 | `WriteReviewSubmit` | Android,Web,IOS | [查看详情](events/WriteReviewSubmit.md) |
| 个人资料保存My Profile页面 | `my_profile_save` | Web | [查看详情](events/my_profile_save.md) |

### 8.【会员】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| m端切换查看各等级卡片 | `ChangeMemberLevel` | level 切换等级<br/>email 用户邮箱 | [查看详情](events/ChangeMemberLevel.md) |
| 会员通知弹窗点击，点最后帧的弹窗上的跳转按钮时上报，中间重复播放动画的点击无需上报 | `MemberNotifDialogClick` | Android,Web,IOS | [查看详情](events/MemberNotifDialogClick.md) |
| 会员通知弹窗关闭 | `MemberNotifDialogClose` | Android,Web,IOS | [查看详情](events/MemberNotifDialogClose.md) |
| 会员通知弹窗展示 | `MemberNotifDialogShow` | Android,Web,IOS | [查看详情](events/MemberNotifDialogShow.md) |
| coupon&giftCard兑换 | `MemberRedeemCharge` | type：coupon | giftcard<br/>id：reward_id<br/>site: 兑换场景，兑换物品详情弹窗、（会员主页、redeem rewards列表页面）这两个使用路径指代、订单结算页<br/>email 用户邮箱<br/>member_level 会员等级<br/>member_points 当前可用积分<br/>error_msg: 兑换失败信息;成功无，失败有 | [查看详情](events/MemberRedeemCharge.md) |
| 点击LP广告位图 | `MembersCenterAdClick` |  | [查看详情](events/MembersCenterAdClick.md) |
| checkout 积分兑换按钮点击 | `MembersCenterCheckoutRedeem` | redeem_coupon_code 兑换的券<br/>redeem_full_text 兑换的券的所有文案 | [查看详情](events/MembersCenterCheckoutRedeem.md) |
| checkout apply my rewards点击 | `MembersCenterCheckoutRewardsClick` |  | [查看详情](events/MembersCenterCheckoutRewardsClick.md) |
| checkout 积分兑换展示 | `MembersCenterCheckoutShow` |  | [查看详情](events/MembersCenterCheckoutShow.md) |
| 点击member rweards | `MembersCenterClick` | type | [查看详情](events/MembersCenterClick.md) |
| 点击促销商品 | `MembersCenterItemClick` | product_handle | [查看详情](events/MembersCenterItemClick.md) |
| 积分兑换-点击物品卡片 | `MembersCenterRedeem` | site 来源：会员主页、redeem rewards列表页面<br/>email 用户邮箱<br/>member_level 会员等级<br/>reward_id 兑换物品ID<br/>member_points 当前可用积分 | [查看详情](events/MembersCenterRedeem.md) |
| 个人中心展示 | `MembersCenterShow` | member_id | [查看详情](events/MembersCenterShow.md) |
| 会员等级优惠券-领取 | `MembersCouponsConvert` | site 来源：会员主页、结算页<br/>coupon_name 券包名<br/>email 用户邮箱<br/>member_level 会员等级 | [查看详情](events/MembersCouponsConvert.md) |
| - **事件英文名**: `MembersEntryClick` | `MembersEntryClick` | type | [查看详情](events/MembersEntryClick.md) |

### 9.【活动】埋点

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 结算页面领取成功跳转，参数同上 | `ActivityManualClick` | Web | [查看详情](events/ActivityManualClick.md) |
| 手动领取活动 | `ActivityManualReceive` | Android,Web,IOS | [查看详情](events/ActivityManualReceive.md) |
| 活动跳链点击 | `ActivityPopupBtnClick` | Android,Web,IOS | [查看详情](events/ActivityPopupBtnClick.md) |
| 活动弹窗展示 （包含浏览未购和老客复购） | `ActivityPopupShow` | Android,Web,IOS | [查看详情](events/ActivityPopupShow.md) |
| - **事件英文名**: `全局商品维度埋点` | `全局商品维度埋点_9活动埋点_2` |  | [查看详情](events/全局商品维度埋点_9活动埋点_2.md) |

### 客户端push

| 事件显示名 | 事件英文名 | 平台 | 文档链接 |
| --- | --- | --- | --- |
| 收到通知时上报 | `MessageReceived` | $url | [查看详情](events/MessageReceived.md) |
| 点击通知时上报 | `NotificationLaunch` | $url | [查看详情](events/NotificationLaunch.md) |
| 上报fcm token | `fcm_token_客户端push_2` | token | [查看详情](events/fcm_token_客户端push_2.md) |

