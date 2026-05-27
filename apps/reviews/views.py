from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.decorators import employee_required
from accounts.permissions import IsEmployee

from .forms import ReviewForm
from .models import Review
from .serializer import ReviewSerializer


def list_reviews(request):
	template_name = 'reviews/list_reviews.html'
	reviews = Review.objects.filter(is_approved=True)
	context = {'reviews': reviews}
	return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_review(request):
	template_name = 'reviews/add_review.html'
	context = {}
	if request.method == 'POST':
		form = ReviewForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('reviews:list_reviews')
	else:
		form = ReviewForm()
	context['form'] = form
	return render(request, template_name, context)


@employee_required
def edit_review(request, id_review):
	template_name = 'reviews/add_review.html'
	review = get_object_or_404(Review, id=id_review)
	if request.method == 'POST':
		form = ReviewForm(request.POST, request.FILES, instance=review)
		if form.is_valid():
			form.save()
			return redirect('reviews:list_reviews')
	else:
		form = ReviewForm(instance=review)
	return render(request, template_name, {'form': form})


@employee_required
def delete_review(request, id_review):
	review = get_object_or_404(Review, id=id_review)
	review.delete()
	return redirect('reviews:list_reviews')


def search_reviews(request):
	template_name = 'reviews/list_reviews.html'
	query = request.GET.get('query', '')
	reviews = Review.objects.filter(
		is_approved=True,
	).filter(
		comment__icontains=query
	)
	context = {'reviews': reviews, 'query': query}
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
