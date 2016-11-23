angular.module('app.preferences').config(preferencesConfig);

preferencesConfig.$inject = ['$stateProvider'];
function preferencesConfig($stateProvider) {
    $stateProvider.state('base.preferences.templatevariables.create', {
        url: '/create',
        views: {
            '@base.preferences': {
                templateUrl: '/messaging/email/templatevariables/create/',
                controller: PreferencesTemplateVariablesCreateUpdate,
            },
        },
        ncyBreadcrumb: {
            label: 'Template variable create',
        },
    });

    $stateProvider.state('base.preferences.templatevariables.edit', {
        url: '/edit/{id:[0-9]{1,}}',
        views: {
            '@base.preferences': {
                templateUrl: function(elem, attr) {
                    return '/messaging/email/templatevariables/update/' + elem.id + '/';
                },
                controller: PreferencesTemplateVariablesCreateUpdate,
                controllerAs: 'vm',
            },
        },
        ncyBreadcrumb: {
            label: 'Template variable edit',
        },
    });
}

angular.module('app.preferences').controller('PreferencesTemplateVariablesCreateUpdate', PreferencesTemplateVariablesCreateUpdate);

PreferencesTemplateVariablesCreateUpdate.$inject = ['$scope'];
function PreferencesTemplateVariablesCreateUpdate($scope) {
    HLInbox.init({textEditorId: 'id_text'});
    HLInbox.initWysihtml5();
    HLEmailTemplates.init({
        parseEmailTemplateUrl: '',
        openVariable: '[[',
        closeVariable: ']]',
        textEditorId: '#id_text',
    });

    // Listen to Angular broadcast function on scope destroy.
    $scope.$on('$destroy', function() {
        // Properly destroy the rich text editor to prevent memory leaks.
        HLInbox.destroyEditor();
    });
}
