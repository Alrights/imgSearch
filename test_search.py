import sift
import imagesearch
import pickle
FEAT_FILE = './ukbench/tmp.sift'
def query_img(img):
	query_img_list = []
	sift.process_image(img,'./ukbench/tmp.sift')
	with open('vocabulary.pkl','rb') as f:
		voc = pickle.load(f)
	index = imagesearch.Indexer('test.db',voc)
	locs,descr = sift.read_features_from_file('./ukbench/tmp.sift')
	index.add_to_index(img,descr)
	index.db_commit()
	src = imagesearch.Searcher('test.db',voc)
	res = src.query(img)[:3]
	for dist, ndx in res:
		imname = src.get_filename(ndx)
		query_img_list.append(imname)
	return query_img_list
if __name__=='__main__':
	img = './ukbench/ukbench00000.jpg'
	res = query_img(img)
	for i in res:
		print i
