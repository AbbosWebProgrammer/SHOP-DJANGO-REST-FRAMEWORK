from rest_framework import routers
from Shop.views import *
from AuthAPP.views import *
from accounts.views import *
from Sitepages.views import *
router = routers.DefaultRouter()

router.register(r'Category',CategoryView,basename='Categor')
router.register(r'Subcategory',SubcategoryView,basename='Subcategory')
router.register(r'Subsubcategory',SubsubcategoryView,basename='Subsubcategory')
router.register(r'Brand',BrandView,basename='Brand')
router.register(r'Product',ProductView,basename='Product')
router.register(r'ProductColor',ProductColorView,basename='ProductColor')
router.register(r'ProductImageFile',ProductImageFileView,basename='ProductImageFile')
router.register(r'ProductSize',ProductSizeView,basename='ProductSize')
router.register(r'Description',DescriptionForProductView,basename='Description')
router.register(r'ProductParamsCaption',ProductParamsCaptionView,basename='ProductParamsCaption')
router.register(r'ProductParamsCaptionitems',ProductParamsCaptionitemsView,basename='ProductParamsCaptionitems')


router.register(r'ProductsColorByProductId',ProductsColorByProductIdView,basename='ProductsColorByProductId')
router.register(r'ProductsColorByProductId',ProductsColorByProductIdView,basename='ProductsColorByProductId')
router.register(r'ImagefilesByProductsColorId',ImagefilesByProductsColorIdView,basename='ImagefilesByProductsColorId')
router.register(r'ProductsizeByProductsColorId',ProductsizeByProductsColorIdView,basename='ProductsizeByProductsColorId')
router.register(r'DescriptionsProductsByProductId',DescriptionsByProductIdView,basename='DescriptionsProductsByProductId')
router.register(r'ProductParamsCaptionByProductId',ProductParamsCaptionByProductIdView,basename='ProductParamsCaptionByProductId')
router.register(r'ProductParamsCaptionitemsByProductParamsCaptionId',ProductParamsCaptionitemsByProductParamsCaptionIdView,basename='ProductParamsCaptionitemsByProductParamsCaptionId')

router.register(r'SubcategoryByCategoryId',SubcategoryByCategoryIdView,basename='SubcategoryByCategoryId')
router.register(r'SubsubcategoryByCategoryId',SubsubcategoryByCategoryIdView,basename='SubsubcategoryByCategoryId')
router.register(r'SubsubcategoryBySubcategorId',SubsubcategoryBySubcategorIdView,basename='SubsubcategoryBySubcategorId')

router.register(r'ProductsByCategoryId',ProductsByCategoryIdView,basename='ProductsBySubCategoryId')
router.register(r'ProductsBySubcategoryId',ProductsBySubcategoryIdView,basename='ProductsBySubcategoryId')
router.register(r'ProductsBySubsubcategoryId',ProductsBySubsubcategoryIdView,basename='ProductsBySubsubcategoryId')
router.register(r'ProductsByBrandId',ProductsByBrandIdView,basename='ProductsByBrandId')

router.register(r'XitProducts',XitProductSView,basename='XitProducts')
router.register(r'ProductInfo',ProductInfoView,basename='ProductInfo')
router.register(r'ProductAllInfo',ProductAllInfoView,basename='ProductAllInfo')

router.register(r'ShoppingDayForHomePageCarousel',ShoppingDayForHomePageCarouselView,basename='ShoppingDayForHomePageCarousel')
router.register(r'MainPagePromoForHomePageSlider',MainPagePromoForHomePageSliderView,basename='MainPagePromoForHomePageSlider')
router.register(r'MainPagePromoForHomePage',MainPagePromoForHomePageView,basename='MainPagePromoForHomePage')
router.register(r'AdvertisingForCategoryMenu',AdvertisingForCategoryMenuView,basename='AdvertisingForCategoryMenu')
router.register(r'ShoppingDayForCategoryCarousel',ShoppingDayForCategoryCarouselView,basename='ShoppingDayForCategoryCarousel')
router.register(r'MainPagePromoForCategory',MainPagePromoForCategoryView,basename='MainPagePromoForCategory')
router.register(r'ShoppingDayForBrandCarousel',ShoppingDayForBrandCarouselView,basename='ShoppingDayForBrandCarousel')
router.register(r'MainPagePromoForBrand',MainPagePromoForBrandView,basename='MainPagePromoForBrand')

router.register(r'ShoppingDayForHomePageCarouselProducts',ShoppingDayForHomePageCarouselProductsView,basename='ShoppingDayForHomePageCarouselProducts')
router.register(r'MainPagePromoForHomePageSliderProducts',MainPagePromoForHomePageSliderProductsView,basename='MainPagePromoForHomePageSliderProducts')
router.register(r'MainPagePromoForHomePageProducts',MainPagePromoForHomePageProductsView,basename='MainPagePromoForHomePageProducts')
router.register(r'AdvertisingForCategoryMenuProducts',AdvertisingForCategoryMenuProductsView,basename='AdvertisingForCategoryMenuProducts')
router.register(r'ShoppingDayForCategoryCarouselProducts',ShoppingDayForCategoryCarouselProductsView,basename='ShoppingDayForCategoryCarouselProducts')
router.register(r'MainPagePromoForCategoryProducts',MainPagePromoForCategoryProductsView,basename='MainPagePromoForCategoryProducts')
router.register(r'ShoppingDayForBrandCarouselProducts',ShoppingDayForBrandCarouselProductsView,basename='ShoppingDayForBrandCarouselProducts')
router.register(r'MainPagePromoForBrandProducts',MainPagePromoForBrandProductsView,basename='MainPagePromoForBrandProducts')

router.register(r'User',UserView,basename='User')
router.register(r'Location',LocationView,basename='Location')
router.register(r'GoodsThatTheCustomerLikes',GoodsThatTheCustomerLikesView,basename='GoodsThatTheCustomerLikes')
router.register(r'Order',OrderView,basename='Order')
router.register(r'OrderDetail',OrderDetailView,basename='OrderDetail')
router.register(r'OrderDetailsByOrderIdView',OrderDetailsByOrderIdView,basename='OrderDetailsByOrderIdView')
router.register(r'QuestionForProduct',QuestionForProductView,basename='QuestionForProduct')
router.register(r'Ansertoquestion',AnsertoquestionView,basename='Ansertoquestion')
router.register(r'Review',ReviewView,basename='Review')
router.register(r'ImagesReview',ImagesReviewView,basename='ImagesReview')
router.register(r'ReviewJson',ReviewJsonView,basename='ReviewJson')



router.register(r'Allcategory',AllcategoriesView,basename='Allcategory')
router.register(r'OrderAndOrderDetailsJson',OrderAndOrderDetailsJsonSerializerView,basename='OrderAndOrderDetailsJson')
router.register(r'AddProductJson',AddProductJsonView,basename='AddProductJson')
router.register(r'SearchProducts',SearchProductsView,basename='SearchProducts')





