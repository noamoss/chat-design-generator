import sys

def messagetemplate(username, message, time, sides):
	talker = sides[0]
	chatmate = sides[1]

	if username == talker["username"]:
		user_is_talker = True
	elif username == chatmate["username"]:
		user_is_talker = False
	else:
		print (sys.stderr, f"unknown username in source file: {username}")
		print(e)
		sys.exit(1)

	if len(message)<=5:
		message+="&nbsp&nbsp&nbsp"             # to keep the message timestamp in online

	if user_is_talker:
		return f"""<div class="d-flex justify-content-start mb-4">
								<div class="img_cont_msg">
									<img src="{ talker['image_url'] }" class="rounded-circle user_img_msg">
								</div>
								<div class="msg_cotainer">
									{ message }
									<span class="msg_time">היום {time}</span>
								</div>
							</div>"""

	else:
		return f"""<div class="d-flex justify-content-end mb-4">
						<div class="msg_cotainer_send">
						  	{message}
							<span class="msg_time_send">היום {time}</span>
						</div>
						<div class="img_cont_msg">
							<img src="{ chatmate['image_url'] }" class="rounded-circle user_img_msg">
						</div>
					</div>
		"""
