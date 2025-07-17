import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useWebSocket } from '../hooks/useWebSocket';

const TeamDashboard = () => {
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateTeam, setShowCreateTeam] = useState(false);
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [collaborationRooms, setCollaborationRooms] = useState([]);
  const [activeRoom, setActiveRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const { connected, sendMessage, lastMessage } = useWebSocket();

  // Form states
  const [teamForm, setTeamForm] = useState({
    name: '',
    description: ''
  });
  const [userForm, setUserForm] = useState({
    username: '',
    email: '',
    password: '',
    role: 'developer',
    team_id: ''
  });

  useEffect(() => {
    fetchCurrentUser();
    fetchTeams();
    fetchUsers();
    fetchCollaborationRooms();
  }, []);

  // WebSocket message handling
  useEffect(() => {
    if (lastMessage) {
      const data = JSON.parse(lastMessage.data);
      
      if (data.type === 'user_joined') {
        console.log('User joined:', data.user);
      } else if (data.type === 'user_left') {
        console.log('User left:', data.user);
      } else if (data.type === 'collaboration_message') {
        setMessages(prev => [...prev, {
          id: Date.now(),
          user: data.user,
          message: data.message,
          timestamp: data.timestamp
        }]);
      }
    }
  }, [lastMessage]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get('/api/enterprise/auth/me');
      if (response.data.success) {
        setCurrentUser(response.data.user);
      }
    } catch (err) {
      console.error('Failed to fetch current user:', err);
    }
  };

  const fetchTeams = async () => {
    try {
      const response = await axios.get('/api/enterprise/teams');
      if (response.data.success) {
        setTeams(response.data.teams || []);
      }
    } catch (err) {
      console.error('Failed to fetch teams:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/enterprise/users');
      if (response.data.success) {
        setUsers(response.data.users || []);
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
  };

  const fetchCollaborationRooms = async () => {
    try {
      const response = await axios.get('/api/enterprise/collaboration/rooms');
      if (response.data.success) {
        setCollaborationRooms(response.data.rooms || []);
      }
    } catch (err) {
      console.error('Failed to fetch collaboration rooms:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/enterprise/teams', teamForm);
      if (response.data.success) {
        setTeams([...teams, response.data.team]);
        setTeamForm({ name: '', description: '' });
        setShowCreateTeam(false);
      }
    } catch (err) {
      setError('Takım oluşturulamadı');
      console.error('Failed to create team:', err);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/enterprise/users', userForm);
      if (response.data.success) {
        setUsers([...users, response.data.user]);
        setUserForm({
          username: '',
          email: '',
          password: '',
          role: 'developer',
          team_id: ''
        });
        setShowCreateUser(false);
      }
    } catch (err) {
      setError('Kullanıcı oluşturulamadı');
      console.error('Failed to create user:', err);
    }
  };

  const joinRoom = (roomId) => {
    if (connected) {
      sendMessage(JSON.stringify({
        type: 'join_room',
        room_id: roomId
      }));
      setActiveRoom(roomId);
      setMessages([]);
    }
  };

  const leaveRoom = () => {
    if (connected && activeRoom) {
      sendMessage(JSON.stringify({
        type: 'leave_room',
        room_id: activeRoom
      }));
      setActiveRoom(null);
      setMessages([]);
    }
  };

  const sendCollaborationMessage = (e) => {
    e.preventDefault();
    if (connected && activeRoom && newMessage.trim()) {
      sendMessage(JSON.stringify({
        type: 'collaboration_message',
        room_id: activeRoom,
        message: newMessage.trim()
      }));
      setNewMessage('');
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin': return 'bg-red-100 text-red-800';
      case 'manager': return 'bg-blue-100 text-blue-800';
      case 'developer': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="context7-loading">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          <p className="mt-4 text-gray-600">Takım verileri yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="team-dashboard min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                👥 Takım Yönetimi
              </h1>
              {currentUser && (
                <div className="ml-4 flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {currentUser.username.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-900">{currentUser.username}</p>
                    <p className={`text-xs px-2 py-1 rounded-full ${getRoleColor(currentUser.role)}`}>
                      {currentUser.role}
                    </p>
                  </div>
                </div>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 ${connected ? 'text-green-600' : 'text-red-600'}`}>
                <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-sm">
                  {connected ? 'Bağlı' : 'Bağlantı Yok'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
            <span className="block sm:inline">{error}</span>
            <button
              onClick={() => setError(null)}
              className="absolute top-0 bottom-0 right-0 px-4 py-3"
            >
              <span className="sr-only">Dismiss</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Teams Section */}
          <div className="lg:col-span-2">
            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-medium text-gray-900">🏢 Takımlar</h2>
                  <button
                    onClick={() => setShowCreateTeam(true)}
                    className="context7-button bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                  >
                    + Yeni Takım
                  </button>
                </div>
              </div>
              <div className="p-6">
                {teams.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">Henüz takım oluşturulmamış</p>
                ) : (
                  <div className="space-y-4">
                    {teams.map((team) => (
                      <div
                        key={team.id}
                        className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                          selectedTeam?.id === team.id
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => setSelectedTeam(team)}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h3 className="text-lg font-medium text-gray-900">{team.name}</h3>
                            <p className="text-sm text-gray-600">{team.description}</p>
                            <div className="flex items-center space-x-4 mt-2">
                              <span className="text-sm text-gray-500">
                                👥 {team.members?.length || 0} üye
                              </span>
                              <span className="text-sm text-gray-500">
                                📅 {new Date(team.created_at).toLocaleDateString('tr-TR')}
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                const roomId = `team_${team.id}`;
                                joinRoom(roomId);
                              }}
                              className="text-blue-600 hover:text-blue-800 p-2 rounded-full hover:bg-blue-50"
                            >
                              💬
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Users Section */}
            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 mt-6">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-medium text-gray-900">👤 Kullanıcılar</h2>
                  <button
                    onClick={() => setShowCreateUser(true)}
                    className="context7-button bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
                  >
                    + Yeni Kullanıcı
                  </button>
                </div>
              </div>
              <div className="p-6">
                {users.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">Henüz kullanıcı oluşturulmamış</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Kullanıcı
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Rol
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Takım
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Son Giriş
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {users.map((user) => (
                          <tr key={user.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center">
                                  <span className="text-white text-sm font-medium">
                                    {user.username.charAt(0).toUpperCase()}
                                  </span>
                                </div>
                                <div className="ml-4">
                                  <div className="text-sm font-medium text-gray-900">{user.username}</div>
                                  <div className="text-sm text-gray-500">{user.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getRoleColor(user.role)}`}>
                                {user.role}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {user.team_id ? teams.find(t => t.id === user.team_id)?.name || 'Bilinmiyor' : 'Takım Yok'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {user.last_login ? new Date(user.last_login).toLocaleDateString('tr-TR') : 'Hiç giriş yapmadı'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Collaboration Section */}
          <div className="lg:col-span-1">
            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">💬 Anlık İşbirliği</h2>
              </div>
              <div className="p-6">
                {activeRoom ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Aktif Oda: {activeRoom}</span>
                      <button
                        onClick={leaveRoom}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        🚪 Çık
                      </button>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto">
                      {messages.length === 0 ? (
                        <p className="text-gray-500 text-center">Henüz mesaj yok</p>
                      ) : (
                        <div className="space-y-3">
                          {messages.map((msg) => (
                            <div key={msg.id} className="bg-white p-3 rounded shadow-sm">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-medium text-gray-900">
                                  {msg.user.username}
                                </span>
                                <span className="text-xs text-gray-500">
                                  {new Date(msg.timestamp).toLocaleTimeString('tr-TR')}
                                </span>
                              </div>
                              <p className="text-sm text-gray-700">{msg.message}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <form onSubmit={sendCollaborationMessage} className="flex space-x-2">
                      <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Mesaj yazın..."
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <button
                        type="submit"
                        disabled={!newMessage.trim()}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
                      >
                        📤
                      </button>
                    </form>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <p className="text-sm text-gray-600">Bir odaya katılın:</p>
                    <div className="space-y-2">
                      {collaborationRooms.map((room) => (
                        <button
                          key={room.id}
                          onClick={() => joinRoom(room.id)}
                          className="w-full text-left p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                        >
                          <div className="font-medium text-gray-900">{room.name}</div>
                          <div className="text-sm text-gray-500">{room.type}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Create Team Modal */}
      {showCreateTeam && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Yeni Takım Oluştur</h3>
            <form onSubmit={handleCreateTeam} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Takım Adı
                </label>
                <input
                  type="text"
                  value={teamForm.name}
                  onChange={(e) => setTeamForm({...teamForm, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Açıklama
                </label>
                <textarea
                  value={teamForm.description}
                  onChange={(e) => setTeamForm({...teamForm, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="3"
                />
              </div>
              <div className="flex space-x-3">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
                >
                  Oluştur
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateTeam(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  İptal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create User Modal */}
      {showCreateUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Yeni Kullanıcı Oluştur</h3>
            <form onSubmit={handleCreateUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Kullanıcı Adı
                </label>
                <input
                  type="text"
                  value={userForm.username}
                  onChange={(e) => setUserForm({...userForm, username: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  E-posta
                </label>
                <input
                  type="email"
                  value={userForm.email}
                  onChange={(e) => setUserForm({...userForm, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Şifre
                </label>
                <input
                  type="password"
                  value={userForm.password}
                  onChange={(e) => setUserForm({...userForm, password: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Rol
                </label>
                <select
                  value={userForm.role}
                  onChange={(e) => setUserForm({...userForm, role: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="viewer">Viewer</option>
                  <option value="developer">Developer</option>
                  <option value="manager">Manager</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Takım
                </label>
                <select
                  value={userForm.team_id}
                  onChange={(e) => setUserForm({...userForm, team_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Takım Seç</option>
                  {teams.map((team) => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex space-x-3">
                <button
                  type="submit"
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700"
                >
                  Oluştur
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateUser(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  İptal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamDashboard; 