# 事件索引

本文件为所有埋点事件的索引，用于EventSchemaTool快速检索相关事件。

## 0.全局埋点

- **ActivityPendantClick** (挂件点击) - Web平台
- **ActivityPendantShow** (活动挂件展示) - Web平台
- **AddToWishlist** (点击加入心愿单) - Android/Web/iOS平台
- **BloomChicClick** (点击BloomChic) - Web平台
- **ChatClick** (点击在线客服按钮) - Web平台
- **CustomizeCookiesResult** (隐私协议，用户是否允许数据收集) - Android/iOS平台
- **HttpResponseError** (Http响应失败) - Android/iOS平台
- **LoginRegisterResult** (登录注册成功) - 服务端
- **NavigationBarClick** (点击导航栏具体栏目) - Web平台
- **NavigationBarShow_NavigationBarHide** (导航栏展示/隐藏) - Web平台
- **PageDataLoadResult** (数据加载结果) - Android/iOS平台
- **PageSwipeUp** (上划页面) - Web平台
- **PasswordResetClick** (密码重置/忘记密码提交点击) - Android/Web/iOS平台
- **PasswordResetPageShow** (密码重置/忘记密码页展示) - Android/Web/iOS平台
- **PasswordResetResult** (密码重置/忘记密码失败) - Android/Web/iOS平台
- **ProductCountdownClick** (活动倒计时点击) - Web平台
- **ProductCountdownShow** (活动倒计时展示) - Web平台
- **RecordWebPerformance** (记录web性能) - Web平台
- **RegisterClick** (注册提交点击) - Android/Web/iOS平台
- **RegisterClickResult** (注册提交失败) - Android/Web/iOS平台
- **RegisterPageShow** (注册页展示) - Android/Web/iOS平台
- **RemoveFromWishlist** (点击移除心愿单) - Android/Web/iOS平台
- **SearchButtonClick** (点击搜索按钮) - Web平台
- **SearchFailed** (搜索请求失败) - Android/Web/iOS平台
- **SearchPredictivePanel** (搜索联想面板展示隐藏) - Web平台
- **SearchResult** (搜索结果上报) - Android/Web/iOS平台
- **SearchWordClick** (搜索联想词点击) - Android/iOS平台
- **ShoppingCartClick** (点击购物车按钮) - Web平台
- **SignInClick** (登录提交点击) - Android/Web/iOS平台
- **SignInClickResult** (登录结果失败) - Android/Web/iOS平台
- **SignInPageShow** (登录页展示) - Android/Web/iOS平台
- **WebviewOverrideUrl** (URL重定向) - Android/iOS平台

## 0.APP特有的埋点

- **APPLaunchPageClick** (APP启屏页点击) - Android/iOS平台
- **APPLaunchPageClose** (APP启屏页关闭) - Android/iOS平台
- **APPLaunchPageShow** (APP启屏页展示) - Android/iOS平台
- **AppLaunch** (APP启动时上报) - Android/iOS平台
- **PushNotificationMessageClick** (点击push通知消息) - Android/iOS平台
- **SwitchSite** (站点切换操作) - Android/iOS平台
- **SwitchSitePageClick** (站点切换弹窗点击) - Android/iOS平台
- **SwitchSitePageShow** (切换站点弹窗展示) - Android/iOS平台
- **af_deeplink_launch** (AppsFlyer回调deeplink成功) - Android/iOS平台
- **af_first_launch** (AF归因成功首次启动) - Android/iOS平台

## 1.【首页】埋点

- **BottomSubscription** (web首页底部订阅) - Web平台
- **CloseButtonClick** (点击关闭按钮) - Web平台
- **CloseConfirmClick** (关闭确认弹窗点击) - Web平台
- **CloseConfirmShow** (关闭确认弹窗展示) - Web平台
- **ContinueShoppingClick** (点击抽奖结果页) - Web平台
- **CouponPopupButtonClick** (转盘前置弹窗点击按钮) - Web平台
- **CouponPopupCloseClick** (转盘前置弹窗点击关闭) - Web平台
- **CouponPopupShow** (转盘前置弹窗展示) - Web平台
- **FrontPageLeave** (离开首页) - Web平台
- **FrontPageShow** (首页展示) - Web平台
- **HomeActivityClick** (首页弹窗点击) - Android/Web/iOS平台
- **HomeActivityShow** (首页弹窗展示) - Android/Web/iOS平台
- **ResourceClick** (点击资源位) - Web平台
- **ResourceShow** (资源位展示) - Android/Web/iOS平台
- **RulesClick** (点击规则条款) - Web平台
- **SMSsubscribe** (footer点击订阅) - Web平台
- **SpinEntryClick** (点击转盘功能入口) - Web平台
- **SpinEntryCloseClick** (转盘功能入口点击关闭) - Web平台
- **SpinEntryShow** (转盘功能入口展示) - Web平台
- **SpinPopupShow** (转盘弹窗页面展示) - Web平台
- **SpinResultShow** (抽奖结果页展示) - Web平台
- **StarSpinTheWheel** (邮箱步骤点击) - Web平台
- **StarSpinTheWheelSMS** (SMS步骤点击抽奖) - Web平台
- **WebRegisterClick** (web注册成功) - Web平台

## 2.【商品】相关埋点

- **AllSelectMyFilter** (全选我的filter) - Android/Web/iOS平台
- **CollectionCarouselchartClick** (LP轮播图模块点击) - Web平台
- **CollectionCategoryTagClick** (LP分类tag位点击) - Web平台
- **CollectionCountdownClick** (LP倒计时点击) - Web平台
- **CollectionFilterlClick** (LP筛选点击) - Web平台
- **CollectionLeave** (离开商品列表) - Android/Web/iOS平台
- **CollectionModelImagelClick** (LP模特图资源位点击) - Web平台
- **CollectionModelSizelClick** (LP模特图选项点击) - Web平台
- **CollectionMultigraphmoduleClick** (LP多图模块点击) - Web平台
- **CollectionResourceShow** (LP资源位展示) - Web平台
- **CollectionShow** (商品列表展示) - Android/Web/iOS平台
- **CollectionTurnPage** (点击翻页) - Web平台
- **DeleteMyFilter** (删除【我的Filter】) - Android/Web/iOS平台
- **FilterClearClick** (点击filter弹窗的清除) - Android/Web/iOS平台
- **FilterClick** (点击[Filter]icon) - Android/Web/iOS平台
- **FilterDoneClick** (点击filter弹窗的提交) - Android/Web/iOS平台
- **FilterSelect** (筛选成功的筛选项) - Android/Web/iOS平台
- **ListViewModeClick** (单列双列切换按钮点击) - Android/Web/iOS平台
- **MyFilterSaveClick** (我的filter保存点击) - Android/Web/iOS平台
- **ProductClick** (点击商品) - Android/Web/iOS平台
- **ProductShow** (商品在列表中的展示) - Android/Web/iOS平台
- **QuickViewClick** (QuickView点击) - Web平台
- **QuickViewShow** (QuickView展示) - Web平台
- **SortMethodClick** (使用某个排序) - Web平台
- **list_skc_click** (列表SKC点击) - Android/Web/iOS平台
- **list_skc_slide** (列表SKC滑动开始) - Android/Web/iOS平台

## 3.【商详页】的埋点

- **AddFromWishlist** (收藏成功) - Android/Web/iOS平台
- **AddToCartClick** (成功加入购物车) - Android/Web/iOS平台
- **AlsoInOurToCart** (商品详情插件搭配销售加购) - Web平台
- **BigPictureClick** (点击查看大图) - Web平台
- **ClickAddCartButton** (点击加入购物车) - Android/Web/iOS平台
- **DetailReviewClick** (点击商品详情页评论区域) - Android/Web/iOS平台
- **FabricCareClick** (Fabric & Care点击) - Android/Web/iOS平台
- **MySizeShow** (size页面展示) - Android/Web/iOS平台
- **ProductAlsoInCartShow** (商品AlsoInCart模块曝光) - Web平台
- **ProductChangeLocationClick** (Shipping & Returns点击change location) - Android/Web/iOS平台
- **ProductCollectClick** (点击收藏) - Android/Web/iOS平台
- **ProductDescriptionImageShow** (商品详情描述图片曝光) - Android/Web/iOS平台
- **ProductDescriptionMediaClick** (Description图文详情模块点击) - Android/Web/iOS平台
- **ProductDescriptionMediaExposure** (商详卖点展示) - Android/Web/iOS平台
- **ProductMediaClick** (商品详情资源媒体点击) - Android/Web/iOS平台
- **ProductMediaExposure** (商品详情资源媒体曝光) - Android/Web/iOS平台
- **ProductModelSizeClick** (点击下拉模特) - Web平台
- **ProductModelSizeSelected** (点击下拉模特选择的选项) - Web平台
- **ProductOptionClick** (商品选项点击) - Android/Web/iOS平台
- **ProductPageLeave** (离开商品详情页) - Android/Web/iOS平台
- **ProductPageLoadFailed** (商品加载失败) - iOS平台
- **ProductPageShow** (商品详情页展示) - Android/Web/iOS平台
- **ProductReturnDetailsClick** (Shipping & Returns点击details) - Android/Web/iOS平台
- **ProductReviewShow** (商详评论展示) - Android/Web/iOS平台
- **ProductShareClick** (分享按钮点击) - Android/Web/iOS平台
- **ProductShippingShow** (商品详情页快递模块曝光) - Android/Web/iOS平台
- **ProductSizeGuideClick** (点击size guide) - Android/Web/iOS平台
- **ProductSizeRecommendationClick** (商品尺码推荐点击) - Android/Web/iOS平台
- **ProductSizeRecommendationResponse** (商品尺码接口响应) - Android/Web/iOS平台
- **ProductSizeRecommendationShow** (商品尺码推荐展示) - Android/Web/iOS平台
- **ProductSupportClick** (商详左下角客服点击) - Android/Web/iOS平台
- **ProductTitleStarClick** (商详页点击商品评分) - Android/Web/iOS平台
- **ProductVariantShow** (商品Variant展示) - Android/Web/iOS平台
- **ProductVideoShow** (商品视频展示) - Android/Web/iOS平台
- **QuickBuyClick** (点击一键加购) - Android/Web/iOS平台
- **ReviewListShow** (评价列表展示) - Android/Web/iOS平台
- **ReviewMediaClick** (点击评论块中图片/视频) - Android/Web/iOS平台
- **ReviewMediaShow** (评论大图曝光) - Android/Web/iOS平台
- **ReviewSortMethodClick** (使用某个排序方式) - Android/Web/iOS平台
- **SizeGuideClick** (点击SizeGuide) - Android/Web/iOS平台
- **VideoPlayStart** (视频播放开始) - Android/Web/iOS平台
- **VideoPlayStop** (视频播放停止) - Android/Web/iOS平台
- **WriteReviewButtonClick** (点击Add Your Review) - Android/Web/iOS平台
- **YouMightAlsoLike** (YouMightAlsoLike展示) - Web平台

## 4.【购物车】埋点

- **BuildMyOutfitClick** (搭配推荐Build My Outfit点击) - Android/Web/iOS平台
- **BuildMyOutfitShow** (搭配推荐Build My Outfit展示) - Android/Web/iOS平台
- **CartAddClick** (点击【ADD】) - Android/iOS平台
- **CartCancelCoupon** (优惠券【X】点击) - Android/iOS平台
- **CartChangeSkuClick** (点击商品的换尺码) - Android/iOS平台
- **CartCouponCopyClick** (券列表页点击Copy) - Android/iOS平台
- **CartCouponsListShow** (券包列表展示) - Android/iOS平台
- **CartCouponsModuleClick** (点击【coupons】) - Android/iOS平台
- **CartDiscountTipsClick** (点击购物车折扣区域) - Android/iOS平台
- **CartEditClick** (点击购物车【编辑】按钮) - Android/iOS平台
- **CartEditDoneClick** (退出编辑) - Android/iOS平台
- **CartEventDiscountShow** (Event Discount展示) - Android/iOS平台
- **CartGiftCardModuleClick** (点击【giftcard】) - Android/iOS平台
- **CartGiftcardListShow** (giftcard列表展示) - Android/iOS平台
- **CartHandCoupon** (手动用券结果) - Android/iOS平台
- **CartOdometerClick** (点击商品计步器【-】) - Android/iOS平台
- **CartShow** (购物车展示) - Android/iOS/M端/PC端平台
- **CartSinginClick** (点击顶部signin横幅) - Android/iOS平台
- **CartSummaryClick** (点击购物【summary】) - Android/iOS平台
- **CartWishlistClick** (点击购物车顶部【收藏夹】按钮) - Android/iOS平台
- **CheckOutClick** (点击Check Out按钮) - Android/Web/iOS平台
- **CheckOutStart** (结算开始) - Android/iOS平台
- **CheckoutCreateFailed** (Checkout接口请求失败) - Android/iOS平台
- **OutfitTypeClick** (搭配商品类型切换tab点击) - Android/Web/iOS平台
- **PreOrderInstructionsClick** (点击pre-order的【?】) - Android/iOS平台
- **ProductCheckOutClick** (商品进入结算) - Android/Web/iOS平台
- **ProductCheckOutStart** (结算开始app端) - Android/iOS平台
- **RemoveFromCart** (点击【delete】) - Android/iOS平台

## 5.【checkout到下单支付】埋点

- **AppReviewShow** (APP评分弹窗展示) - Android/iOS平台
- **BackToCartClick** (点击Back to cart) - Android/Web平台
- **ChangeButtonClick** (点击Change按钮) - Android/Web平台
- **CheckoutFinish** (支付结果，手机端专属) - Android/iOS平台
- **CheckoutPageClick** (勾选订阅) - Android/Web/iOS平台
- **CheckoutPageShow** (结算页展示) - Android/Web/iOS平台
- **CheckoutPageStart** (结算页面一进入) - Android/Web/iOS平台
- **CheckoutRewardsApply** (结算-券&giftcard应用) - Web平台
- **CheckoutRewardsEntryClick** (结算-兑换入口点击) - Web平台
- **CheckoutRewardsEntryShow** (结算-兑换入口展示) - Web平台
- **CheckoutRewardsLogin** (结算-奖品登录入口点击) - Web平台
- **CheckoutRewardsRedeem** (结算-券&giftcard兑换) - Web平台
- **CheckoutShippingSelect** (选择邮寄方式) - Android/Web/iOS平台
- **CheckoutTrustpilotClick** (tp入口点击事件) - Web平台
- **CheckoutTrustpilotShow** (tp入口展示) - Android/Web/iOS平台
- **CouponApplied** (应用优惠或礼品卡) - Android/Web/iOS平台
- **DownloadAppClick** (web页面导下载点击) - Web平台
- **DownloadAppPopClick** (web端导下载APP弹窗点击) - Web平台
- **DownloadAppPopShow** (web端导下载APP弹窗展示) - Web平台
- **DownloadAppShow** (web页面导下载展示) - Web平台
- **NotNowClick** (关闭按钮点击) - Android/iOS平台
- **OrderQuickClick** (订单快捷查询模块点击) - Android/iOS平台
- **OrderQuickClose** (订单快捷查询模块关闭) - Android/iOS平台
- **OrderQuickShow** (订单快捷查询模块展示) - Android/iOS平台
- **OrderSummaryClick** (点击Order summary) - Web平台
- **PayNowButtonClick** (点击Pay now) - Android/Web/iOS平台
- **PaymentComplete** (支付完成) - Android/Web平台
- **PaymentSuccessShow** (ThankYou页展示) - Android/Web/iOS平台
- **PlaceAnOrder** (点击Pay now下单) - Web平台
- **ProductPurchaseSuccess** (商品支付成功详情（商品纬度）) - 服务端
- **PurchaseSuccess** (订单支付成功) - 服务端
- **PushPermissionPopClick** (AppPush前置引导弹窗点击) - Android/iOS平台
- **PushPermissionPopResult** (AppPush前置引导通知权限结果) - Android/iOS平台
- **PushPermissionPopShow** (AppPush前置引导弹窗展示) - Android/iOS平台
- **SendAsGiftClick** (礼品卡SendAsGift按钮点击) - Android/iOS平台
- **SendFeedbackFailed** (Feedback上传失败) - Android/iOS平台
- **SendFeedbackSuccess** (Feedback上传成功) - Android/iOS平台
- **UseCouponDialogClick** (订单页展示用券提示弹窗点击) - Web平台
- **UseCouponDialogShow** (订单页展示用券提示弹窗展示) - Web平台
- **UseCouponResult** (使用券结果) - Web平台
- **YesReviewClick** (Yes按钮点击) - Android/iOS平台
- **add_payment_info** (点击Pay now添加支付信息) - Web平台
- **fcm_token** (Firebase PUSH Token) - Android/iOS平台

## 6.【退货退款】埋点

- **PartialRefundOnlyClick** (部分仅退款弹窗按钮点击) - Android/Web/iOS平台
- **PartialRefundOnlyPopup** (部分仅退款弹窗曝光) - Android/Web/iOS平台
- **ProductRefundSuccess** (退款成功) - 服务端
- **ProductReturn** (商品退货) - 服务端
- **ProductReturnSuccess** (退货成功) - 服务端
- **RefundPage** (进入退货页面) - Android/Web/iOS平台
- **RefundSubmitPage** (退货退款预提交页面曝光) - Android/Web/iOS平台
- **SelectRefundItemsPage** (选择退货商品页面曝光) - Android/Web/iOS平台
- **SelectReturnReasonNextClick** (选择退货原因【下一步】按钮点击) - Android/Web/iOS平台
- **SelectReturnReasonPage** (选择退货原因页面曝光) - Android/Web/iOS平台

## 6.【me页】埋点

- **AddressClick** (地址库地址) - Android/iOS平台
- **FeedbackEntranceClick** (Feedback点击) - Android/Web/iOS平台
- **FeedbackEntranceShow** (Feedback展示) - Android/Web/iOS平台
- **FeedbackSubmit** (Feedback提交按钮) - Android/iOS平台
- **MeClick** (个人中心Me点击) - Android/iOS平台
- **MeShow** (个人中心Me展示) - Android/iOS平台
- **MineMenuItemClick** (我的菜单项点击) - Android/iOS/M端平台
- **MyAccountClick** (我的账号点击) - Android/iOS平台
- **MyCouponsClick** (优惠券中心点击) - Android/iOS平台
- **MyMenuClick** (个人中心我的菜单点击) - Android/iOS平台
- **MyOrdersClick** (我的订单点击) - Android/iOS平台
- **MyProfileClick** (点击个人信息编辑按钮) - Android/iOS/M端平台
- **MyReviewsClick** (我的评论点击) - Android/iOS平台
- **MyWishlistClick** (我的收藏夹点击) - Android/iOS平台
- **SignRegisterClick** (登录注册入口点击) - Android/iOS平台
- **TrackDeliveredClick** (点击【delivered】) - M端平台
- **TrackDetailsClick** (点击【details】) - M端平台
- **TrackInTransitClick** (点击【in transit】) - M端平台
- **WriteReviewSubmit** (评论提交后上报) - Android/Web/iOS平台
- **my_profile_save** (个人资料保存My Profile页面) - Web平台

## 8.【会员】埋点

- **ChangeMemberLevel** (m端切换查看各等级卡片) - M端平台
- **MemberNotifDialogClick** (会员通知弹窗点击) - Android/Web/iOS平台
- **MemberNotifDialogClose** (会员通知弹窗关闭) - Android/Web/iOS平台
- **MemberNotifDialogShow** (会员通知弹窗展示) - Android/Web/iOS平台
- **MemberRedeemCharge** (coupon&giftCard兑换) - 全平台
- **MembersCenterAdClick** (点击LP广告位图) - 全平台
- **MembersCenterCheckoutRedeem** (checkout积分兑换按钮点击) - 全平台
- **MembersCenterCheckoutRewardsClick** (checkout apply my rewards点击) - 全平台
- **MembersCenterCheckoutShow** (checkout积分兑换展示) - 全平台
- **MembersCenterClick** (点击member rewards) - 全平台
- **MembersCenterItemClick** (点击促销商品) - 全平台
- **MembersCenterRedeem** (积分兑换-点击物品卡片) - 全平台
- **MembersCenterShow** (个人中心展示) - 全平台
- **MembersCouponsConvert** (会员等级优惠券-领取) - 全平台
- **MembersEntryClick** (会员入口点击) - 全平台

## 9.【活动】埋点

- **ActivityManualClick** (结算页面领取成功跳转) - Web平台
- **ActivityManualReceive** (手动领取活动) - Android/Web/iOS平台
- **ActivityPopupBtnClick** (活动跳链点击) - Android/Web/iOS平台
- **ActivityPopupShow** (活动弹窗展示) - Android/Web/iOS平台

## 客户端push

- **MessageReceived** (收到通知时上报) - Android/iOS平台
- **NotificationLaunch** (点击通知时上报) - Android/iOS平台
- **fcm_token** (上报fcm token) - Android/iOS平台
