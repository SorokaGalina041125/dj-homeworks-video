import pytest
from django.urls import reverse
from model_bakery import baker
from students.models import Course


pytestmark = pytest.mark.django_db


class TestCourseAPI:
    """Тесты для API курсов"""
    
    def test_get_course_retrieve(self, api_client, course_factory):
        """Проверка получения одного курса"""
        course = course_factory(name="Python Basic")
        url = reverse('courses-detail', args=[course.id])
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['id'] == course.id
    
    def test_get_courses_list(self, api_client, course_factory):
        """Проверка получения списка курсов"""
        course_factory(_quantity=3)
        url = reverse('courses-list')
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 3
    
    def test_filter_courses_by_id(self, api_client, course_factory):
        """Проверка фильтрации по id"""
        courses = course_factory(_quantity=5)
        target = courses[2]
        url = reverse('courses-list')
        response = api_client.get(url, {'id': target.id})
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == target.id
    
    def test_filter_courses_by_name(self, api_client, course_factory):
       """Проверка фильтрации по name (точное совпадение)"""
       course_factory(name="Python Basic")
       course_factory(name="Django Advanced")
       url = reverse('courses-list')
       response = api_client.get(url, {'name': 'Python Basic'})
       
       assert response.status_code == 200
       assert len(response.data) == 1
       assert response.data[0]['name'] == 'Python Basic'
    
    def test_create_course_success(self, api_client):
        """Тест создания курса"""
        url = reverse('courses-list')
        data = {'name': 'New Course'}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert Course.objects.count() == 1
    
    def test_update_course_success(self, api_client, course_factory):
        """Тест обновления курса"""
        course = course_factory(name="Old Name")
        url = reverse('courses-detail', args=[course.id])
        response = api_client.patch(url, {'name': 'New Name'}, format='json')
        
        assert response.status_code == 200
        assert response.data['name'] == 'New Name'
    
    def test_delete_course_success(self, api_client, course_factory):
        """Тест удаления курса"""
        course = course_factory()
        url = reverse('courses-detail', args=[course.id])
        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert Course.objects.count() == 0