'use strict';

var app = angular.module('PrimeResume', ['ui.bootstrap']);

app.factory('resourceDataService', function ($http, $modal) {
    var resourceDataFactory = {};
    var _submit = function (data) {
        return $http.post('/api/apply', data).success(
            function (results) {
                window.location = '/careers/apply_success';
            }).error(
            function (results) {
                var modalInstance = $modal.open({
                  templateUrl: 'myModalContent.html',
                  controller: ModalInstanceCtrl,
                  size: 'lg',
                  resolve: {
                    data: function () {
                      return angular.toJson(data);
                    }
                  }
                });

                modalInstance.result.then(function () {
                    console.log('Modal dismissed0 at: ' + new Date());
                }, function () {
                    console.log('Modal dismissed at: ' + new Date());
                });

                return results;
            });
    };

    resourceDataFactory.submit = _submit;

    return resourceDataFactory
});

app.controller('resumeController', function ($scope, $modal, resourceDataService) {
    $scope.languageOptions = ['english', 'spanish', 'french'];
    $scope.languageLevels = ['beginner', 'intermediate', 'fluent', 'native'];
    $scope.skillLevels = ['beginner', 'intermediate', 'senior', 'expert'];

    $scope.name = '';
    $scope.email = '';
    $scope.telephone = '';
    $scope.experiences = [{}];
    $scope.educations = [{}];
    $scope.skills = [{}];
    $scope.languages = [{}];
    $scope.certifications = [{}];

    $scope.addItem = function (type) {
        if(type === 'experience') {
            $scope.experiences.push({});
        } else if (type === 'education') {
            $scope.educations.push({});
        } else if (type === 'skill') {
            $scope.skills.push({});
        } else if (type === 'language') {
            $scope.languages.push({});
        } else if (type === 'certification') {
            $scope.certifications.push({});
        }
    };

    $scope.removeItem = function (type, item) {
        console.log('deleting ' + item);
        var index = $scope[type].indexOf(item);
        if (index != -1) {
            $scope[type].splice(index, 1);
        }
    };

    $scope.opened = false;

    $scope.open = function(item, $event, src) {
        console.log('click');
        $event.preventDefault();
        $event.stopPropagation();

        item[src + '_opened'] = true;
    };

    $scope.dateOptions = {
        datepickerMode: 'month',
        minMode: 'month',
        showWeeks: false
    };

    $scope.sending = false;

    $scope.submit = function() {
        if ($scope.applicationForm.$valid) {
            $scope.sending = true;
            resourceDataService.submit({
                name: $scope.name,
                email: $scope.email,
                telephone: $scope.telephone,
                experiences: $scope.experiences,
                educations: $scope.educations,
                skills: $scope.skills,
                languages: $scope.languages,
                certifications: $scope.certifications
            });
        }
    };

    $scope.cancel = function() {
     $scope.sending = false;
    };
});


var ModalInstanceCtrl = function ($scope, $modalInstance, data) {
  $scope.data = data;

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
};
