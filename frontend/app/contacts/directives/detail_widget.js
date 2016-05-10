angular.module('app.contacts.directives').directive('contactDetailWidget', contactDetailWidget);

function contactDetailWidget() {
    return {
        restrict: 'E',
        scope: {
            contact: '=',
            height: '=',
        },
        templateUrl: 'contacts/directives/detail_widget.html',
        controller: ContactDetailWidgetController,
        controllerAs: 'vm',
        bindToController: true,
    };
}

ContactDetailWidgetController.$inject = ['HLResource', 'Settings'];
function ContactDetailWidgetController(HLResource, Settings) {
    var vm = this;

    vm.settings = Settings;

    vm.updateModel = updateModel;

    function updateModel(data, field) {
        var accounts = [];
        var args = HLResource.createArgs(data, field, vm.contact);

        if (field === 'twitter' || field === 'linkedin') {
            args = {
                id: vm.contact.id,
                social_media: [args],
            };
        }

        if (data.hasOwnProperty('accounts')) {
            data.accounts.forEach(function(account) {
                accounts.push(account.id);
            });

            data.accounts = accounts;
        }

        return HLResource.patch('Contact', args).$promise;
    }
}

