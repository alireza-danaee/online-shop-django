superuser = User.objects.filter(is_superuser=True).values_list('email')
		product = self.comment.content_object
		author_email = superuser
		user_email = self.comment.user.email
		current_site = get_current_site(self.request)
		if author_email == user_email:
			author_email = False
			user_email = False
		parent_email = False

		if self.comment.parent:
			parent_email = self.comment.parent.user.email
			if parent_email in [author_email , user_email]:
				parent_email = False

		if author_email:
			message = "دیدگاه جدیدی برای محصول {} ارسال شد \n {}{}".format(product.name , current_site , reverse('shop:product_detail' , kwargs={"slug":product.slug} ))
			email = EmailMessage(
					"دیدگاه جدید", 
					message, 
					to=[author_email]
		)
		email.send()

		if user_email:
			mail_subject = "دریافت دیدگاه شما "
			message = "دیدگاه شما دریافت شد و به زودی به آن پاسخ میدهیم با تشکر از شما"
			email = EmailMessage(
						mail_subject,
						message,
						to=[user_email]
			)
			email.send()

		if parent_email:
			mail_subject = "پاسخ به دیدگاه شما"
			message = "شخص به دیدگاه شما پاسخ داد اگر مایلید میتوانید آن را ببینید. \n{}{}".format(current_site , reverse('shop:product_detail' , kwargs={"slug":product.slug} ))
			email = EmailMessage(
						mail_subject,
						message,
						to=[parent_email]
			)
			email.send()