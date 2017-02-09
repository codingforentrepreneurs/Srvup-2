from courses.models import Course


def copy_courses(qs=Course.objects.all()):
    if qs.count() < 100:
        for obj in qs:
            user        = obj.user
            title       = obj.title
            image       = obj.image
            category    = obj.category
            secondary   = obj.secondary.all()
            description = obj.description
            price       = obj.price
            new_obj = Course.objects.create(
                user = user,
                title = title,
                image = image,
                category = category,
                
                description = description,
                price = price
            )
            #new_obj.secondary = secondary
            for cat in secondary:
                new_obj.secondary.add(cat)
            new_obj.save()
        qs2 = Course.objects.all()
        if qs2.count() <= 100:
            return copy_courses(qs=qs2)
    return qs.count()


copy_courses()