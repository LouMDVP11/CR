from django.urls import path,re_path
from .CRUDS.ViewAchievment import *
from .CRUDS.ViewBloodCampaing import *
from .CRUDS.ViewBloodDonationCampaingLogs import *
from .CRUDS.ViewBloodOutflow import *
from .CRUDS.ViewBloodType import *
from .CRUDS.ViewCampaignReceiver import *
from .CRUDS.ViewCampaignBloodType import *
from .CRUDS.ViewDonation import *
from .CRUDS.ViewDonationLog import *
from .CRUDS.ViewDonationType import *
from .CRUDS.ViewDonor import *
from .CRUDS.ViewDonorAchievment import *
from .CRUDS.ViewDonorSuspendedLog import *
from .CRUDS.ViewEmployee import *
from .CRUDS.ViewEthnicGroup import *
from .CRUDS.ViewMotive import *
from .CRUDS.ViewPerson import *
from .CRUDS.ViewPersonalDonation import *
from .CRUDS.ViewPosition import *
from .CRUDS.ViewPublicaction import *
from .CRUDS.ViewPublicationLog import *
from .CRUDS.ViewReceiver import *
from .CRUDS.ViewCity import *
from .CRUDS.ViewProvince import *
from .CRUDS.ViewDonationReceiverCampaign import *


urlpatterns = [
    #URL DEPARTAMENTOS
    path('achievment/',AchievmentV.as_view(), name='Achievment_list'),
    path('achievment/<int:id>', UpdateAchievement.as_view(), name='Achievmient_update'),
    
    path('bloodDonationCampaing/',BloodDonationCampaignView.as_view(), name='BloodCampaing_list'),
    path('bloodDonationCampaing/<int:id>', BloodDonationCampaignView.as_view(), name='BloodCampaing_process'),
    path('updateStateCampaing/',UpdateStateCampaignView.as_view(), name='UpdateStateCampaing_list'),
    path('updateStateCampaing/<int:id>', UpdateStateCampaignView.as_view(), name='UpdateStateCampaing_process'),
    path('reportBloodCampaign/<int:id>', CampaignsReportsView.as_view(), name='CampaignsReportsView'),   

    path('boodDonationCampingLog/',BoodDonationCampingLogView.as_view(), name='BloodDonationCampaingLog_list'),
    path('boodDonationCampingLog/<int:id>', BoodDonationCampingLogView.as_view(), name='BloodDonationCampaingLog_process'),

    path('bloodOutflow/',BloodOutflow.as_view(), name='BloodOutflow_list'),
    path('bloodOutflow/<int:id>', BloodOutflow.as_view(), name='BloodOutflow_process'),
    
    path('bloodtype/',BloodTypeView.as_view(), name='bloodtypBloodOutflowe_list'),
    path('bloodtype/<int:id>', BloodTypeView.as_view(), name='bloodtype_process'),

    path('campaingReceive/',CampaignReceiverView.as_view(), name='CampaingReceive_list'),
    path('campaingReceive/<int:id>', CampaignReceiverView.as_view(), name='CampaingReceive_process'),
    path('receiversCampaign/<int:id>', ReceiverOfCampaignView.as_view(), name='ReceiversOfCampaign_process'),
    
    path('campaingBloodType/',CampaignBloodTypeView.as_view(), name='campaingBloodType_list'),
    path('campaingBloodType/<int:id>', CampaignBloodTypeView.as_view(), name='campaingBloodType_process'),

    path('donation/',DonationView.as_view(), name='donation_list'),
    path('donation/<int:id>', DonationView.as_view(), name='donation_process'),
    path('donationsCampaign/', GetDonationsCampaignView.as_view(), name='donationCampaign_list'),
    path('donationsCampaign/<int:id>', GetDonationsCampaignView.as_view(), name='donationCampaign_process'),
    path('donation/updateState/<int:id>', updateStateDonationView.as_view(), name='updateStateDonation_process'),
    path('donation/completeFalse/<int:id>', GetDonationsCompleteFalseView.as_view(), name='getDonationCompleteFalse_process'),

    path('donation/searchByDate/', GetDonationsByDateView.as_view(), name='GetDonationsByDateView'),

    path('donationsPersonalCR/<int:id>', GetDonationsDonorView.as_view(), name='getDonationsPersonalCR_process'),


    path('donationLog/',DonationlogV.as_view(), name='donationLog_list'),
    path('donationLog/<int:id>', DonationlogV.as_view(), name='donationLog_process'),

    path('donationType/',DonationTypeView.as_view(), name='donationType_list'),
    path('donationType/<int:id>', DonationTypeView.as_view(), name='donationType_process'),

    path('donor/',DonorView.as_view(), name='donor_list'),
    path('donor/<int:id>', DonorView.as_view(), name='donor_process'),
    path('donor/suspend/<int:id>',SuspendDonor.as_view(), name='donor_suspend'),
    path('donor/activate/<int:id>',ActivateDonor.as_view(), name='donor_activate'),
    path('donor/searchByPerson/<int:idPerson>',SearchByPersonId.as_view(), name='donor_byPerson'),
    path('donor/updateDonor/<int:id>',UpdateDonor.as_view(), name='donor_update'),
    path('donor/updateBT/<int:id>',UpdateBT.as_view(), name='donor_update_bt'),
    path('donor/updateBlood/<int:id>',UpdateBloodDonor.as_view(), name='donor_update'),

    path('donorAchievment/',DonorAchievmentView.as_view(), name='donorAchievment_list'),
    path('donorAchievment/<int:id>', DonorAchievmentView.as_view(), name='donorAchievment_process'),

    path('donorSuspendedLog/',DonorSuspendedLogView.as_view(), name='donorSuspendedLog_list'),
    path('donorSuspendedLog/<int:id>', DonorSuspendedLogView.as_view(), name='donorSuspendedLog_process'),

    path('employee/',EmployeeView.as_view(), name='employee_list'),
    path('employee/<int:id>', EmployeeView.as_view(), name='employee_process'),

    path('ethnicGroup/',EthnicGroupView.as_view(), name='ethnicGroup_list'),
    path('ethnicGroup/<int:id>', EthnicGroupView.as_view(), name='ethnicGroup_process'),

    path('motive/',MotiveView.as_view(), name='person_list'),
    path('motive/<int:id>', MotiveView.as_view(), name='person_process'),

    path('person/',PersonView.as_view(), name='person_list'),
    path('person/<int:id>', PersonView.as_view(), name='personsignin_process'),
    path('person/sign-in/',PersonSignIn.as_view(), name='personsignin_list'),
    path('person/sign-in/<int:id>', PersonSignIn.as_view(), name='person_process'),
    path('person/updateperson/<int:id>', UpdatePersonNoPassword.as_view(), name='personupdate_process'),
    path('person/allData/<int:id>', getAllData.as_view(), name='personGetAllData'),
    path('person/lookpassword/<int:id>', VerifyUserPassword.as_view(), name='lookpassword_process'),
    path('person/updateType/<int:id>', UpdateTypeView.as_view(), name='personupdatetype_process'),
    path('person/getLastId/', selectLastIdView.as_view(), name='selectLasId_process'),
    path('person/searchPersonDpi/<int:id>', searchByDPI.as_view(), name='searchByDpi_process'),
    path('person/updateCredentials/<int:id>', UpdateCredentialsUser.as_view(), name='searchByDpi_process'),
    re_path('person/searchByIdExtranjero/(?P<id>[\w-]+)$', searchByIdExtranjero.as_view(), name='searchByIdExtranjero_process'),
    path('person/updateEmployeeNoPass/<int:id>', UpdateEmployeeNoPassword.as_view(), name='updateEmployeeNoPass_process'),
    path('person/verifyPassword/<int:id>', VerifyPasswordView.as_view(), name='changePassword_process'),
    path('person/recovery/', PersonRecoveryView.as_view(), name='Recovery_process'),
    path('person/user/<int:id>', UpdateUserView.as_view(), name='updateUser_process'),
    path('person/getDonor/', SearchByDPIorIdView.as_view(), name='getDonor_process'),


    path('personalDonation/',PersonalDonationView.as_view(), name='personalDonation_list'),
    path('personalDonation/<int:id>', PersonalDonationView.as_view(), name='personalDonation_process'),
    path('personalDonationId/<int:id>', PersonalDonationIDView.as_view(), name='personalDonationId_process'),
    path('updateStatePersonalDonation/<int:id>', UpdateSataetePersonaDonationView.as_view(), name='updatePersonalDonationState_process'),
    path('personalsinuser/',PostPerson.as_view(), name='personalDonation_list'),


    path('position/',PositionView.as_view(), name='position_list'),
    path('position/<int:id>', PositionView.as_view(), name='position_process'),

    path('publication/',PublicationView.as_view(), name='publication_list'),
    path('publication/<int:id>', PublicationView.as_view(), name='publication_process'),
    path('updatepublication/',UpdatePublicationView.as_view(), name='updatepublication_list'),
    path('updatepublication/<int:id>', UpdatePublicationView.as_view(), name='updatepublication_process'),
    path('updatepublicationnp/<int:id>', UpdatePublicationNPView.as_view(), name='updatepublicationnp_process'),
    path('publicationLog/',PublicationLogView.as_view(), name='publicationLog_list'),
    path('publicationLog/<int:id>', PublicationLogView.as_view(), name='publicationLog_process'),

    path('receiver/',ReceiverView.as_view(), name='receiver_list'),
    path('receiver/<int:id>', ReceiverView.as_view(), name='receiver_process'),
    path('receiversNoAsignados/<int:id>', ReceiverNoAsignadosView.as_view(), name='receiver_process'),
    path('receiverState/<int:id>', UpdateStateView.as_view(), name='receiver_list'),

    path('city/',CityView.as_view(), name='city_list'),
    path('city/<int:id>', CityView.as_view(), name='city'),
    path('city/searchByProvinceId/<int:idProvince>', SearchByProvinceId.as_view(), name='city'),

    path('province/',ProvinceView.as_view(), name='province_list'),
    path('province/<int:id>', ProvinceView.as_view(), name='province_process'),

    path('donationReceiver/',DonationReceiverCampaignView.as_view(), name='province_list'),
    path('donationReceiver/<int:id>', DonationReceiverCampaignView.as_view(), name='province_process'),
    path('donationIdReceiver/<int:id>', DonationIDReceiverView.as_view(), name='province_process'),
      
]