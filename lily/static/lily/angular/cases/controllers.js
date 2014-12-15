/**
 * caseControllers is a container for all case related Controllers
 */
angular.module('caseControllers', [
    // Angular dependencies
    'ngCookies',

    // 3rd party
    'ui.bootstrap',

    // Lily dependencies
    'caseServices'
])

    /**
     * CaseListController controller to show list of accounts
     *
     */
    .controller('CaseListController', [
        '$scope',
        '$cookieStore',
        '$window',

        'Case',
        'Cookie',
        function($scope, $cookieStore, $window, Case, Cookie) {

            Cookie.prefix ='caseList';

            /**
             * table object: stores all the information to correctly display the table
             */
            $scope.table = {
                page: 1,  // current page of pagination: 1-index
                pageSize: 20,  // number of items per page
                totalItems: 0, // total number of items
                filter: Cookie.getCookieValue('filter', ''),  // search filter
                archived: Cookie.getCookieValue('archived', false),
                order:  Cookie.getCookieValue('order', {
                    ascending: true,
                    column:  'expires'  // string: current sorted column
                }),
                visibility: Cookie.getCookieValue('visibility', {
                    caseId: true,
                    client: true,
                    subject: true,
                    priority: true,
                    type: true,
                    status: true,
                    expires: true,
                    assignedTo: true,
                    tags: true
                })};

            /**
             * updateTableSettings() sets scope variables to the cookie
             */
            function updateTableSettings() {
                Cookie.setCookieValue('filter', $scope.table.filter);
                Cookie.setCookieValue('archived', $scope.table.archived);
                Cookie.setCookieValue('order', $scope.table.order);
                Cookie.setCookieValue('visibility', $scope.table.visibility);
            }

            /**
             * updateAccounts() reloads the accounts trough a service
             *
             * Updates table.items and table.totalItems
             */
            function updateCases() {
                Case.query(
                    $scope.table
                ).then(function(data) {
                        $scope.table.items = data.accounts;
                        $scope.table.totalItems = data.total;
                    }
                );
            }

            /**
             * Watches the model info from the table that, when changed,
             * needs a new set of accounts
             */
            $scope.$watchGroup([
                'table.page',
                'table.order.column',
                'table.order.ascending',
                'table.filter',
                'table.archived'
            ], function() {
                updateTableSettings();
                updateCases();
            });

            /**
             * Watches the model info from the table that, when changed,
             * needs to store the info to the cache
             */
            $scope.$watchCollection('table.visibility', function() {
               updateTableSettings();
            });

            /**
             * setFilter() sets the filter of the table
             *
             * @param queryString string: string that will be set as the new filter on the table
             */
            $scope.setFilter = function(queryString) {
                $scope.table.filter = queryString;
            };

            $scope.toggleArchived = function() {
                $scope.table.archived = !$scope.table.archived;
            }
        }
    ]
);
