from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import IsEmployee

from .forms import ReviewForm
from .models import Review
from .serializer import ReviewSerializer


def list_reviews(request):
    template_name = 'reviews/list_reviews.html'
    reviews = Review.objects.select_related('reservation__guest').all()
    user_review_ids = set()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_review_ids = set(reviews.values_list('id', flat=True))
        else:
            guest = getattr(request.user, 'guest_profile', None)
            if guest:
                user_review_ids = set(
                    Review.objects.filter(reservation__guest=guest).values_list('id', flat=True)
                )

    context = {'reviews': reviews, 'user_review_ids': user_review_ids}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_review(request):
    template_name = 'reviews/add_review.html'
    context = {}
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('reviews:list_reviews')
    else:
        form = ReviewForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def edit_review(request, id_review):
    template_name = 'reviews/add_review.html'
    review = get_object_or_404(Review, id=id_review)
    guest = getattr(request.user, 'guest_profile', None)
    is_owner = guest and review.reservation.guest == guest
    if not request.user.is_superuser and not is_owner:
        return redirect('reviews:list_reviews')
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('reviews:list_reviews')
    else:
        form = ReviewForm(instance=review, user=request.user)
    return render(request, template_name, {'form': form})


@login_required(login_url='/accounts/login/')
def delete_review(request, id_review):
    if not request.user.is_superuser:
        return redirect('reviews:list_reviews')
    review = get_object_or_404(Review, id=id_review)
    review.delete()
    return redirect('reviews:list_reviews')


def search_reviews(request):
    template_name = 'reviews/list_reviews.html'
    query = request.GET.get('query', '')
    reviews = Review.objects.select_related('reservation__guest').filter(comment__icontains=query)
    user_review_ids = set()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_review_ids = set(reviews.values_list('id', flat=True))
        else:
            guest = getattr(request.user, 'guest_profile', None)
            if guest:
                user_review_ids = set(
                    reviews.filter(reservation__guest=guest).values_list('id', flat=True)
                )

    context = {'reviews': reviews, 'query': query, 'user_review_ids': user_review_ids}
    return render(request, template_name, context)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment']
    ordering_fields = ['rating', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsEmployee()]

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Review.objects.filter(is_approved=True)
        return Review.objects.all()
