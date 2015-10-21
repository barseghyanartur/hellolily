angular.module('app.forms.directives').directive('formPhoneNumbers', formPhoneNumbers);

function formPhoneNumbers() {
    return {
        restrict: 'E',
        require: '^form',
        scope: {
            phoneNumbers: '=',
            addRelatedField: '&',
            removeRelatedField: '&',
        },
        templateUrl: 'forms/directives/phone_numbers.html',
        controller: FormPhoneNumbersController,
        controllerAs: 'vm',
        bindToController: true,
        link: function(scope, element, attrs, form) {
            // Set parent form on the scope
            scope.form = form;
        },
    };
}

FormPhoneNumbersController.$inject = ['$rootScope'];
function FormPhoneNumbersController($rootScope) {
    var vm = this;
    vm.telephoneTypes = [
        {key: 'work', value: 'Work'},
        {key: 'mobile', value: 'Mobile'},
        {key: 'home', value: 'Home'},
        {key: 'fax', value: 'Fax'},
        {key: 'other', value: 'Other'},
    ];
    vm.sidebar = $rootScope.$$childHead.emailSettings.sidebar.form;

    vm.formatPhoneNumber = formatPhoneNumber;

    function formatPhoneNumber(phoneNumber) {
        // Format telephone number
        if (phoneNumber.raw_input.match(/[a-z]|[A-Z]/)) {
            // If letters are found, skip formatting: it may not be a phone field after all
            return false;
        }

        // Check if it's a mobile phone number
        if (phoneNumber.raw_input.match(/^\+31([\(0\)]+)?6|^06/)) {
            // Set phone number type to mobile
            phoneNumber.type = 'mobile';
        }

        var newNumber = phoneNumber.raw_input
            .replace('(0)', '')
            .replace(/\s|\(|\-|\)|\.|\\|\/|\–|x|:|\*/g, '')
            .replace(/^00/, '+');

        if (newNumber.length === 0) {
            return false;
        }

        if (!newNumber.startsWith('+')) {
            if (newNumber.startsWith('0')) {
                newNumber = newNumber.substring(1);
            }

            newNumber = '+31' + newNumber;
        }

        if (newNumber.startsWith('+310')) {
            newNumber = '+31' + newNumber.substring(4);
        }

        phoneNumber.raw_input = newNumber;
    }
}
