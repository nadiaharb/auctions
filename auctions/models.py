from django.contrib.auth.models import AbstractUser
from django.db import models



my_categories = (
    ('Fashion', 'Fashion'),
    ('Books, Movies & Music', 'Books, Movies & Music'),
    ('Electronics', 'Electronics'),
    ('Collectibles & Art', 'Collectibles & Art'),
    ('Home & Garden', 'Home & Garden'),
    ('Sporting Goods', 'Sporting Goods'),
    ('Toys & Hobbies', 'Toys & Hobbies'),
    ('Business & Industrial', 'Business & Industrial'),
    ('Health & Beauty', 'Health & Beauty'),
    ('Others', 'Others')

)

class User(AbstractUser):


    def __str__(self):
        return self.username

class NewListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.DecimalField('Starting Bid $',max_digits=4, decimal_places=2, )

    category = models.CharField(max_length=200, choices=my_categories)
    image = models.URLField(blank=True, null=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    openbid = models.BooleanField(default=True)


    def __str__(self):
        return self.title

class Category(models.Model):
    category = models.CharField(max_length=200, choices=my_categories)

    def __str__(self):
        return self.category

class ActiveListings(models.Model):
    name = models.ForeignKey(NewListing,on_delete=models.CASCADE)

    openbid=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.user)

    @property
    def get_items(self):
        wathclistitems=self.watchlistitem_set.all()
        total=sum([item.quantity for item in wathclistitems])
        return total



class WatchlistItem(models.Model):
    product = models.ForeignKey(NewListing, on_delete=models.SET_NULL, blank=True, null=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.product)


class Comment(models.Model):
    title=models.ForeignKey(NewListing, related_name='comments', on_delete=models.CASCADE, editable=False)
    username=models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    body=models.TextField('', max_length=2000)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Auction(models.Model):
    title = models.ForeignKey(NewListing, on_delete=models.CASCADE)
    no_of_bids=models.IntegerField()
    start=models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return str(self.title)



class Bid(models.Model):
    title = models.ForeignKey(NewListing, on_delete=models.CASCADE, related_name='product',editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    bidValue=models.DecimalField('Bid $',decimal_places=2, max_digits=7)
    bid_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)



