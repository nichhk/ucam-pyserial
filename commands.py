SYNC = 'aa0d00000000'
ACK_ID = 'aa0e'
INITIAL_ID = 'aa01'
GET_PICTURE_ID = 'aa04'
SNAPSHOT_ID = 'aa05'
DATA_ID = 'aa0a'
SET_PKG_SIZE_ID = 'aa06'
RESET_ID = 'aa08'

def sync():
	return SYNC

def initial(img_format, raw_res, jpeg_res):
	return _build(INITIAL_ID, '00', img_format, raw_res, jpeg_res)

def data(data_type, len1, len2, len3):
	return _build(DATA_ID, data_type, len1, len2, len3)

def set_pkg_size(pkg_size_lo, pkg_size_hi):
	return _build(SET_PKG_SIZE_ID, '08', pkg_size_lo, pkg_size_hi, '00')

def snapshot(snapshot_type, skip_frame_lo, skip_frame_hi):
	return _build(SNAPSHOT_ID, snapshot_type, skip_frame_lo,
			skip_frame_hi, '00')

def get_picture(pic_type):
	return _build(GET_PICTURE_ID, pic_type, '00', '00', '00')

def ack(cmd_id, ack_counter, pkg_id1='00', pkg_id2='00'):
	return _build(ACK_ID, cmd_id, ack_counter, pkg_id1, pkg_id2)

def reset(reset_type='00'):
	return _build(RESET_ID, reset_type, '00', '00', 'FF')

def _build(cmd_id, p1, p2, p3, p4):
	return ''.join([cmd_id, p1, p2, p3, p4])

