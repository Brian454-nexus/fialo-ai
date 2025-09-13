import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/authStore';
import { useUserStore } from '../store/userStore';
import { ArrowLeftIcon, UserIcon, BuildingOfficeIcon, MapPinIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

export const ProfilePage: React.FC = () => {
  const { user } = useAuthStore();
  const { profile } = useUserStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <div className="px-6 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="flex items-center mb-6">
              <Button variant="ghost" className="mr-4">
                <ArrowLeftIcon className="w-4 h-4 mr-2" />
                Back to Dashboard
              </Button>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
                {profile?.userType === 'company' ? (
                  <BuildingOfficeIcon className="w-10 h-10 text-white" />
                ) : (
                  <UserIcon className="w-10 h-10 text-white" />
                )}
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Profile Settings
              </h1>
              <p className="text-gray-600">
                Manage your account and preferences
              </p>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Profile Information */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="lg:col-span-2"
            >
              <Card>
                <CardHeader>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Personal Information
                  </h3>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="label">Full Name</label>
                      <input
                        type="text"
                        value={user?.name || ''}
                        className="input"
                        readOnly
                      />
                    </div>
                    <div>
                      <label className="label">Email Address</label>
                      <input
                        type="email"
                        value={user?.email || ''}
                        className="input"
                        readOnly
                      />
                    </div>
                  </div>

                  <div>
                    <label className="label">User Type</label>
                    <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                      {profile?.userType === 'company' ? (
                        <BuildingOfficeIcon className="w-5 h-5 text-secondary-600 mr-2" />
                      ) : (
                        <UserIcon className="w-5 h-5 text-primary-600 mr-2" />
                      )}
                      <span className="font-medium capitalize">
                        {profile?.userType === 'company' ? 'Waste Company' : 'Individual User'}
                      </span>
                    </div>
                  </div>

                  {profile?.companyName && (
                    <div>
                      <label className="label">Company Name</label>
                      <input
                        type="text"
                        value={profile.companyName}
                        className="input"
                        readOnly
                      />
                    </div>
                  )}

                  <div>
                    <label className="label">Location</label>
                    <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                      <MapPinIcon className="w-5 h-5 text-gray-400 mr-2" />
                      <span>{profile?.location || 'Not specified'}</span>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-gray-200">
                    <Button variant="outline">
                      <Cog6ToothIcon className="w-4 h-4 mr-2" />
                      Edit Profile
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Account Settings */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-6"
            >
              <Card>
                <CardHeader>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Account Settings
                  </h3>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start">
                    Change Password
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    Notification Settings
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    Privacy Settings
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Data & Export
                  </h3>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start">
                    Export Data
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    Download Reports
                  </Button>
                </CardContent>
              </Card>

              <Card className="border-red-200">
                <CardHeader>
                  <h3 className="text-lg font-semibold text-red-900">
                    Danger Zone
                  </h3>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50">
                    Delete Account
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};
