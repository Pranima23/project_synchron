from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group


class IndividualCardUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to add remarks for individual members in a standup card
    """
    # member = serializers.SlugRelatedField(slug_field='user', read_only=True)
    member_name = serializers.SerializerMethodField('_get_member_name')
    member_position = serializers.SerializerMethodField('_get_member_position')

    def _get_member_name(self, member_update_obj):
        if member_update_obj.member is not None:
            fname = member_update_obj.member.user.first_name
            lname = member_update_obj.member.user.last_name
            return f"{fname} {lname}"
        
    def _get_member_position(self, member_update_obj):
        if member_update_obj.member is not None:
            return member_update_obj.member.position.position_name
            
            
    class Meta:
        model = IndividualCardUpdate
        fields = ['updated_at', 'member', 'member_name', 'member_position', 'remarks']  


class StandupCardSerializer(serializers.ModelSerializer):
    """
    A serializer for standup cards
    """
    team = serializers.SlugRelatedField(slug_field='team_name', queryset=Team.objects.all())
    individual_updates = IndividualCardUpdateSerializer(many=True)

    
    
    class Meta:
        model = StandupCard
        fields = ['id', 'team', 'standup_date', 'release_cycle', 'sprint_id', 'individual_updates', 'notes']

    def create(self, validated_data):

        """ Creates standup card instance and related individual update instances """

        updates_data = validated_data.pop('individual_updates')

        # SM (user) can create standup card for his/her team only unlike superuser
        current_user = self.context['request'].user
        team = validated_data.pop('team')
        if not current_user.is_superuser:
            team = self.context['request'].user.synchron_user.team

        #----- Create standup card instance
        standup_card = StandupCard.objects.create(team=team, **validated_data)

        #----- Create individual member update for standup card instances and relate with the standup card

        # No individual updates provided, set empty remarks for all members
        if updates_data == []:
            for member in team.team_members.all():
                if member.user.groups.filter(name='Scrum Member').exists():
                    # print("remarks created for ", member)
                    IndividualCardUpdate.objects.create(standup_card=standup_card, member=member, remarks="")
        
        # Individual updates for all scrum members
        elif len(updates_data)+1 == team.team_members.count():
            for update_data in updates_data:
                # print("remarks created for", update_data.get('member'))
                IndividualCardUpdate.objects.create(standup_card=standup_card, **update_data)

        # Individual updates for some scrum members
        else:       
            for member in team.team_members.all():
                if member.user.groups.filter(name='Scrum Member').exists():
                    for update_data in updates_data:
                        if member == update_data.get('member'):
                            # print("remarks created for ", member, update_data.get('remarks'))
                            IndividualCardUpdate.objects.create(standup_card=standup_card, **update_data)
                        else:
                            # print("remarks created for ", member, "empty remarks")
                            IndividualCardUpdate.objects.create(standup_card=standup_card, member=member, remarks="")   
    
        return standup_card
    
    def update(self, instance, validated_data):

        """ Updates standup card instance and related individual remarks update instances """

        updates_data = validated_data.pop('individual_updates')
        updates = instance.individual_updates

        # Update instance of standup card, team can't be updated
        instance.release_cycle = validated_data.get('release_cycle', instance.release_cycle)
        instance.sprint_id = validated_data.get('sprint_id', instance.sprint_id)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()

        # Update instances of individual member updates for standup card
        for update_instance in updates.all():
            for update in updates_data:
                # Update according to matched member
                if update_instance.member == update.get('member'):                                        
                    update_instance.member = update.get('member', update_instance.member)
                    update_instance.remarks = update.get('remarks', update_instance.remarks)
            update_instance.save()              

        return instance


# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = ['id', 'position_name']


# class TeamSerializer(serializers.ModelSerializer):
#     # members = serializers.SlugRelatedField(many=True, slug_field='user', read_only=True)
#     class Meta:
#         model = Team
#         fields = ['id', 'team_name']


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class SynchronUserSerializer(serializers.ModelSerializer):
#     team = serializers.SlugRelatedField(slug_field='team_name', read_only=True)
#     position = serializers.SlugRelatedField(slug_field='position_name', read_only=True)
#     user = serializers.SlugRelatedField(slug_field='username', read_only=True)
#     class Meta:
#         model = SynchronUser
#         fields = ['user', 'team', 'position']
#         depth = 1


# class SyncupBoardSerializer(serializers.ModelSerializer):
#     # team = serializers.HyperlinkedRelatedField(view_name='team-detail', queryset=Team.objects.all())
    
#     class Meta:
#         model = SyncupBoard
#         fields = ['id', 'team', 'description']     