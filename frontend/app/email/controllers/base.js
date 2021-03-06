angular.module('app.email').config(emailConfig);
emailConfig.$inject = ['$stateProvider', '$urlRouterProvider'];
function emailConfig($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.when('/email',  ['$state', 'Settings', function($state, Settings) {
        if (Settings.email.previousInbox) {
            // If we previously selected a certain inbox, redirect to that inbox.
            $state.transitionTo(Settings.email.previousInbox.state, Settings.email.previousInbox.params, false);
        } else {
            // Otherwise just go to the main inbox.
            $state.transitionTo('base.email.list', {labelId: 'INBOX'});
        }
    }]);

    $stateProvider.state('base.email', {
        url: '/email',
        views: {
            '@': {
                templateUrl: 'email/controllers/base.html',
                controller: EmailBaseController,
                controllerAs: 'vm',
            },
            'labelList@base.email': {
                templateUrl: 'email/controllers/label_list.html',
                controller: 'LabelListController',
                controllerAs: 'vm',
            },
            'createAccount@base.email': {
                templateUrl: 'accounts/controllers/form.html',
                controller: 'AccountCreateController',
                controllerAs: 'vm',
                resolve: {
                    currentAccount: function() {
                        return null;
                    },
                },
            },
            'showAccount@base.email': {
                controller: EmailShowAccountController,
            },
            'createContact@base.email': {
                templateUrl: 'contacts/controllers/form.html',
                controller: 'ContactCreateUpdateController',
                controllerAs: 'vm',
                resolve: {
                    currentContact: function() {
                        return null;
                    },
                },
            },
            'showContact@base.email': {
                controller: EmailShowContactController,
            },
            'createCase@base.email': {
                templateUrl: 'cases/controllers/form.html',
                controller: 'CaseCreateUpdateController',
                controllerAs: 'vm',
                resolve: {
                    currentCase: function() {
                        return null;
                    },
                    teams: ['UserTeams', function(UserTeams) {
                        return UserTeams.query().$promise;
                    }],
                },
            },
            'createDeal@base.email': {
                templateUrl: 'deals/controllers/form.html',
                controller: 'DealCreateUpdateController',
                controllerAs: 'vm',
                resolve: {
                    currentDeal: function() {
                        return null;
                    },
                    teams: ['UserTeams', function(UserTeams) {
                        return UserTeams.query().$promise;
                    }],
                },
            },
        },
        ncyBreadcrumb: {
            label: 'Email',
        },
        resolve: {
            primaryEmailAccountId: ['$q', 'User', function($q, User) {
                var deferred = $q.defer();
                User.me(null, function(data) {
                    deferred.resolve(data.primary_email_account);
                });
                return deferred.promise;
            }],
        },
        onExit: ['Settings', function(Settings) {
            // Reset the email page when we navigate away from the email views.
            Settings.email.page = 0;
        }],
    });
}

angular.module('app.email').controller('EmailBaseController', EmailBaseController);

EmailBaseController.$inject = ['Settings'];
function EmailBaseController(Settings) {
    Settings.page.setAllTitles('custom', 'Email');

    activate();

    //////

    function activate() {
        Settings.email.resetEmailSettings();
    }
}

angular.module('app.email').controller('EmailShowAccountController', EmailShowAccountController);
EmailShowAccountController.$inject = ['$scope', 'Account', 'Contact', 'Settings'];
function EmailShowAccountController($scope, Account, Contact, Settings) {
    $scope.$watch('settings.email.sidebar.account', function(newValue, oldValue) {
        if (oldValue === 'showAccount' && newValue === 'checkAccount' && Settings.email.data.account.id) {
            activate();
        }
    }, true);

    activate();

    function activate() {
        Account.get({id: Settings.email.data.account.id}).$promise.then(function(account) {
            $scope.account = account;
            $scope.contactList = Contact.search({filterquery: 'accounts.id:' + Settings.email.data.account.id});
            $scope.contactList.$promise.then(function(contactList) {
                $scope.contactList = contactList.objects;
            });
        });
    }
}

angular.module('app.email').controller('EmailShowContactController', EmailShowContactController);
EmailShowContactController.$inject = ['$scope', 'Contact', 'Settings'];
function EmailShowContactController($scope, Contact, Settings) {
    $scope.$watch('settings.email.sidebar.contact', function(newValue, oldValue) {
        if (oldValue === 'showContact' && newValue === 'checkContact' && Settings.email.data.contact.id) {
            activate();
        }
    }, true);

    activate();

    function activate() {
        Contact.get({id: Settings.email.data.contact.id}).$promise.then(function(contact) {
            $scope.contact = contact;
            $scope.height = 300;

            if ($scope.contact.accounts) {
                $scope.contact.accounts.forEach(function(account) {
                    var colleagueList = Contact.search({filterquery: 'NOT(id:' + $scope.contact.id + ') AND accounts.id:' + account.id});
                    colleagueList.$promise.then(function(colleagues) {
                        account.colleagueList = colleagues.objects;
                    });
                });

                if ($scope.contact.accounts.length >= 2) {
                    $scope.height = 91;
                }
            }
        });
    }
}
