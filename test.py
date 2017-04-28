import flask
from PIL import Image
import cStringIO as StringIO
import urllib
import exifutil
import os
import sift
import imagesearch
import pickle
import json
import urllib2
UPLOAD_FOLDER = './ukbench/img/'
FEAT_FILE = './ukbench/tmp.sift'
app = flask.Flask(__name__)
@app.route('/')
def index():
	return flask.render_template('index.html', has_result=False)
@app.route('/classify_upload',methods=['POST'])
def classify_upload():
	imagefile = flask.request.files['imagefile']
	filename = os.path.join(UPLOAD_FOLDER,imagefile.filename)
	imagefile.save(filename)
	image = exifutil.open_oriented_im(filename)
	result = {0:'s',1:'t',2:'y'}
	query_img_list = query_img2(filename)
	print filename
	return flask.render_template('index.html', has_result=True, result=result,imagesrc=embed_image_html(image),query_img=query_img_list)
def get_img_classify_res():
	url = 'http://192.168.116.131:8080'
	res = urllib2.urlopen(url).read()
	dict_res = json.loads(res)
	bef_res = {}
	for key in dict_res.keys():
		bef_res[key] = float(dict_res[key])
	final_res = sorted(bef_res.iteritems(),key=lambda d:d[1],reverse=True)
	return final_res
def embed_image_html(image):
    """Creates an image embedded in HTML base64 format."""
    image_pil = Image.fromarray((255 * image).astype('uint8'))
    image_pil = image_pil.resize((256, 256))
    string_buf = StringIO.StringIO()
    image_pil.save(string_buf, format='png')
    data = string_buf.getvalue().encode('base64').replace('\n', '')
    res = 'data:image/png;base64,' + data
    string_buf.close()
    return res
def query_img(img):
	query_img_list = []
	sift.process_image(img,FEAT_FILE)
	with open('vocabulary.pkl','rb') as f:
		voc = pickle.load(f)
	index = imagesearch.Indexer('test.db',voc)
	locs,descr = sift.read_features_from_file(FEAT_FILE)
	index.add_to_index(img,descr)
	index.db_commit()
	src = imagesearch.Searcher('test.db',voc)
	res = src.query(img)[:3]
	for dist, ndx in res:
		imname = src.get_filename(ndx)
		print imname
		exifutil_img = exifutil.open_oriented_im(imname)
		img_embed = embed_image_html(exifutil_img)
		query_img_list.append(img_embed)
	return query_img_list
def query_img2(img):
	query_img_list = []
	sift.process_image(img,FEAT_FILE)
	with open('tianchi1.pkl','rb') as f:
		voc = pickle.load(f)
	index = imagesearch.Indexer('tianchi.db',voc)
	locs,descr = sift.read_features_from_file(FEAT_FILE)
	index.add_to_index(img,descr)
	index.db_commit()
	src = imagesearch.Searcher('tianchi.db',voc)
	res = src.query(img)[:4]
	for dist, ndx in res:
		imname = src.get_filename(ndx)
		print imname
		exifutil_img = exifutil.open_oriented_im(imname)
		img_embed = embed_image_html(exifutil_img)
		query_img_list.append(img_embed)
	return query_img_list
if __name__ == '__main__':
	app.debug = True
	app.run(host='202.204.54.218')
	#app.run()