from flask import Flask, json
import helpers

def respondWithItem(data, transformer='transform', statusCode=200, message = 'Success', hint=''):
	response = dict(())
	response['data'] = getattr(data, transformer)()
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'DDT_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithCollection(data, transformer='transform', statusCode = 200, message = 'Success', hint=''):
    response_data = []
    response = dict(())
    for item in data:
        response_data.append(getattr(item, transformer)()) 
    response['data'] = response_data
    response['code'] = statusCode
    response['notification'] = {
        'feedCode' : 'DDT_'+str(statusCode),
        'message' : message,
        'hint' : hint,
        'type' : 'success'
    }
    response['version'] = 1
    return json.jsonify(response)

def respondWithArray(data, statusCode = 200, message = 'Success', hint=''):
	response = dict(())
	response['data'] = data
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'DDT_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithPaginatedCollection(data, meta, statusCode = 200, message = 'Success', hint=''):
	response = dict(())
	response['data'] = data
	response['code'] = statusCode
	response['meta'] = {
		'pagination' : {
			'count' : meta['count'],
			'current_page' : meta['current_page'],
			'per_page' : meta['per_page'],
			'total' : meta['total'],
			'links' : {
				'prev_page' :  helpers.modify_url(meta['links']['prev_page']) if meta['links']['prev_page'] is not None else None,
				'next_page' : helpers.modify_url(meta['links']['next_page']) if meta['links']['next_page'] is not None else None
			},
			'total_page' : meta['total_page'],
		}
	}
	response['notification'] = {
		'feedCode' : 'DDT_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondOk(message = 'Success', statusCode = 200, hint=''):
	response = dict(())
	response['data'] = []
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'DDT_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithError(message = 'Error', statusCode = 500, hint=''):
	response = dict(())
	response['data'] = []
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'DDT_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'error'
	}
	response['version'] = 1
	return json.jsonify(response)
