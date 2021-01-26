from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserListSerializer, 
    UserEditSerializer, 
    RestaurantSerializer,
    RestaurantCreateSerializer,
    ReviewListSerializer,
    ReviewCreateSerializer, 
    ReplyListSerializer,
    ReplyCreateSerializer,
)

from .models import User, Restaurant, Review, Reply


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        user_uid = User.objects.all().filter(email=request.data['email'])[0].uid

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'], 
                    'uid': user_uid
                }
            }

            return Response(response, status=status_code)



class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)


class UserDeleteView(APIView): 
    permission_classes = (IsAuthenticated,)  

    def get(self, request): 
        user = request.user
        user_uid = request.query_params.get('user_uid')  
        
        if user.role == 1: 
            User.objects.filter(uid=user_uid).delete() 

            response = {
                'success': True, 
                'status_code': status.HTTP_200_OK, 
                'message': "User was deleted successfully!" 
            }
            return Response(response, status=status.HTTP_200_OK) 

        else: 
            response = {
                'success': False,  
                'status_code': status.HTTP_403_FORBIDDEN, 
                'message': "You cannot detele this user!" 
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)


class UserEditView(APIView): 
    permission_classes = (IsAuthenticated,) 

    def post(self, request): 
        user = request.user 

        if user.role == 1: 
            User.objects.filter(uid=request.data['uid']).update(email=request.data['email'])

            status_code = status.HTTP_200_OK 

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User is successfully deleted!',
                'user': request.data['uid']
            }
            return Response(response, status=status_code) 

class UserEditView1(APIView): 
    serializer_class = UserEditSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request): 
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True) 

        if request.user.role == 1: 
            if valid: 
                User.objects.filter(uid=serializer.data['user_uid']).update(email=serializer.data['email'])
                status_code = status.HTTP_200_OK

                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'User is successfully deleted!',
                    'user': serializer.data
                }
                return Response(response, status=status_code)
            else: 
                status_code = status.HTTP_403_FORBIDDEN

                response = {
                    'success': False,
                    'statusCode': status_code,
                    'message': 'User is not deleted!', 
                    'user': []
                }
                return Response(response, status=status_code)
        else: 
            status_code = status.HTTP_403_FORBIDDEN

            response = {
                    'success': False,
                    'statusCode': status_code,
                    'message': 'User is successfully deleted!',
                    'user': []
            }
            return Response(response, status=status_code)


    
#------------------------------Restaurant--------------------------------#

class RestaurantListView(APIView): 
    serializer_class = RestaurantSerializer
    permission_classes = (AllowAny,) 

    def get(self, request):
        user = request.user
        if user.role == 2:
            restaurants = Restaurant.objects.all() 
            reviews = Review.objects.all() 

            owners_restaurants = []
            avg_rate = 0.0

            for res in restaurants:  
                if res.owner.uid == user.uid: 
                    avg_rate = 0.0
                    count = 0

                    for rev in reviews: 
                        if rev.restaurant.id == res.id:
                            count = count + 1 
                            avg_rate = avg_rate + rev.rate 
                    
                    if count != 0: 
                        res.overall_rating = (avg_rate / count)
                    else: 
                        res.overall_rating = 0.0

                    res.unread_reviews = len(Review.objects.all().filter(restaurant=res.id, has_reply=False))
                    owners_restaurants.append(res) 

                    
            # print ("Mana bu yerda") 

            serializer = self.serializer_class(owners_restaurants, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched owners restaurants',
                'restaurants': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
        else: 
            restaurants = Restaurant.objects.all()
            reviews = Review.objects.all()

            rated_restaurants = [] 
            avg_rate = 0.0 

            for res in restaurants:
                avg_rate = 0.0
                count = 0 

                for rev in reviews: 
                    if rev.restaurant.id == res.id:
                        count = count + 1 
                        avg_rate = avg_rate + rev.rate 
                
                if count != 0: 
                    res.overall_rating = (avg_rate / count)
                else: 
                    res.overall_rating = 0.0
                
                
                res.unread_reviews = -1             
                rated_restaurants.append(res)

            serializer = self.serializer_class(rated_restaurants, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched restaurants',
                'restaurants': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)



class RestaurantCreate(APIView): 
    serializer_class = RestaurantCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        #serializer['owner'] = user.uid
        valid = serializer.is_valid(raise_exception=True)

        if user.role == 2:
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED

                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Restaurant successfully registered!',
                    'restaurant': serializer.data
                }

                return Response(response, status=status_code)
        else: 
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You were not registered as an owner!'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)


#------------------------------Reviews--------------------------------#

class ReviewCreateView(APIView): 
    serializer_class = ReviewCreateSerializer 
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # user = request.user
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Review successfully registered!',
                'review': serializer.data
            }            
            return Response(response, status=status_code)

        else: 
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'Your review was not created.', 
                'review': []
            }
            return Response(response, status.HTTP_403_FORBIDDEN)



class ReviewListView(APIView):
    serializer_class = ReviewListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        restaurant = self.request.query_params.get('restaurant')
        
        print(restaurant)

        if user.role == 7:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action', 
                'reviews': []
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            reviews = Review.objects.all()
            
            ########
            reviews_list = [] 

            for rev in reviews: 
                if rev.restaurant.id == int(restaurant):
                    reviews_list.append(rev) 
            ########

            serializer = self.serializer_class(reviews_list, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched reviews',
                'reviews': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)


#------------------------------Replies--------------------------------#

class ReplyCreateView(APIView): 
    serializer_class = ReplyCreateSerializer 
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        data = request.data 
 
        review = Review.objects.all().filter(id=data['review']) 
        restaurant = Restaurant.objects.all().filter(id=review[0].restaurant.id)

        # print (restaurant[0].owner.uid)
        # print (user.uid)
        # print (restaurant[0].owner.uid == user.uid)

        serializer = self.serializer_class(data=data)
        valid = serializer.is_valid(raise_exception=True)
        
        if (restaurant[0].owner.uid == user.uid): 
            if review[0].has_reply == False: 
                if valid:
                    serializer.save()
                    Review.objects.filter(id=review[0].id).update(has_reply=True)

                    status_code = status.HTTP_201_CREATED

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Reply successfully registered!',
                        'reply': serializer.data
                    }            
                    return Response(response, status=status_code)

                else: 
                    response = {
                        'success': False,
                        'statusCode': status.HTTP_403_FORBIDDEN,
                        'message': 'Your reply was not created.', 
                        'reply': {"review": -1, "reply_text": "", "date_of_reply": ""}
                    }
                    return Response(response, status.HTTP_403_FORBIDDEN)
            else: 
                response = {
                    'success': False,
                    'statusCode': status.HTTP_403_FORBIDDEN,
                    'message': 'Review was replied', 
                    'reply': {"review": -1, "reply_text": "", "date_of_reply": ""}
                }
                return Response(response, status.HTTP_403_FORBIDDEN)

        else: 

            response = {
                    'success': False,
                    'statusCode': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not owner of this restaurant. You cannot write reply',
                    'reply': {"review": -1, "reply_text": "", "date_of_reply": ""}
            }            
            return Response(response, status=status.HTTP_403_FORBIDDEN)



class ReplyListView(APIView):
    serializer_class = ReplyListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        
        if user.role == 7:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            reviews = Reply.objects.all()
            serializer = self.serializer_class(reviews, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched reviews',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

# Delete reply 

class ReplyDeleteView(APIView):
    permission_classes = (IsAuthenticated,) 

    def get(self, request): 
        user = request.user
        reply_id = self.request.query_params.get('reply_id') 

        if user.role == 1: 
            # deleting_reply = Reply.objects.all().filter(id=reply_id)
            # review_id = Review.objects.filter(id=deleting_reply[0].review.id)

            # Review.objects.filter(id=review_id).update(has_reply=False) 
            Reply.objects.filter(id=reply_id).delete() 

            response = {
                'success': True, 
                'status_code': status.HTTP_200_OK, 
                'message': "Reply was deleted!" 
            }
            return Response(response, status=status.HTTP_200_OK) 
        else: 
            response = {
                'success': False,  
                'status_code': status.HTTP_403_FORBIDDEN, 
                'message': "You cannot detele this reply!" 
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN) 