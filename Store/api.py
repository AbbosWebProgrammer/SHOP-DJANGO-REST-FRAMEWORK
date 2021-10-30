from rest_framework import routers
from Shop.views import *
from AuthAPP.views import *
from accounts.views import *


router = routers.DefaultRouter()

router.register(r'Category',CategoryView,basename='Category')
router.register(r'Subcategory',SubcategoryView,basename='Subcategory')
router.register(r'Brand',BrandView,basename='Brand')
router.register(r'Products',ProductsView,basename='Products')
router.register(r'ProductColor',ProductColorView,basename='ProductColor')
router.register(r'Imagefiles',ImagefilesView,basename='Imagefiles')
router.register(r'ProductSize',ProductSizeView,basename='ProductSize')
router.register(r'Description',DescproductView,basename='Description')
router.register(r'ProductParamsCaption',ProductParamsCaptionView,basename='ProductParamsCaption')
router.register(r'ProductParamsCaptionitems',ProductParamsCaptionitemsView,basename='ProductParamsCaptionitems')

router.register(r'SubcategoryByCategoryId',SubcategoryByCategoryIdView,basename='SubcategoryByCategoryId')
router.register(r'ProductsBySubcategoryId',ProductsBySubcategoryIdView,basename='ProductsBySubcategoryId')
router.register(r'ProductsColorByProductId',ProductsColorByProductIdView,basename='ProductsColorByProductId')
router.register(r'ProductsColorByProductId',ProductsColorByProductIdView,basename='ProductsColorByProductId')
router.register(r'ImagefilesByProductsColorId',ImagefilesByProductsColorIdView,basename='ImagefilesByProductsColorId')
router.register(r'ProductsizeByProductsColorId',ProductsizeByProductsColorIdView,basename='ProductsizeByProductsColorId')
router.register(r'DescProductsByProductId',DescProductsByProductIdView,basename='DescProductsByProductId')
router.register(r'ProductParamsCaptionByProductId',ProductParamsCaptionByProductIdView,basename='ProductParamsCaptionByProductId')
router.register(r'ProductParamsCaptionitemsByProductParamsCaptionId',ProductParamsCaptionitemsByProductParamsCaptionIdView,basename='ProductParamsCaptionitemsByProductParamsCaptionId')


router.register(r'User',UserView,basename='User')
router.register(r'Location',LocationView,basename='Location')
router.register(r'CustomerLike',CustomerLikeView,basename='CustomerLike')
router.register(r'Customercard',CustomercardView,basename='Customercard')
router.register(r'Orders',OrdersView,basename='Orders')
router.register(r'Order_details',Order_detailsView,basename='Order_details')
router.register(r'Order_detailsByOrderIdView',Order_detailsByOrderIdView,basename='Order_detailsByOrderIdView')
router.register(r'Question',QuestionView,basename='Question')
router.register(r'Ansertwoquestion',AnsertwoquestionView,basename='Ansertwoquestion')
router.register(r'Review',ReviewView,basename='Review')
router.register(r'ImagesReview',ImagesReviewView,basename='ImagesReview')


router.register(r'Main_page_promo',Main_page_promoView,basename='Main_page_promo')
router.register(r'Main_page_banner',Main_page_bannerView,basename='Main_page_banner')
router.register(r'XitProducts',XitProductSView,basename='XitProducts')





