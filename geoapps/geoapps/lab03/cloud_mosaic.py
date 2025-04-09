import ee

ee.Initialize(project='ee-kamilmolo13')

def create_cloud_free_mosaic(aoi, start_date, end_date):
    image_collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
    .filterDate(start_date, end_date) \
    .filterBounds(aoi) \

    def cloud_mask(image):
        qa_band = image.select('QA60')
        cloud_bit = 1 << 10
        cirrus_bit = 1 << 11
        c_mask = qa_band.bitwiseAnd(cloud_bit).eq(0).And(qa_band.bitwiseAnd(cirrus_bit).eq(0))
        return image.updateMask(c_mask).copyProperties(image, image.propertyNames())
    
    mosaic = image_collection.map(cloud_mask).median().clip(aoi)

    return mosaic