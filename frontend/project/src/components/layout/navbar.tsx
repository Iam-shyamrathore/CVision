import { BriefcaseIcon, FileTextIcon, HomeIcon, UsersIcon } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Home', to: '/', icon: HomeIcon },
  { name: 'Job Descriptions', to: '/jobs', icon: BriefcaseIcon },
  { name: 'CVs', to: '/cvs', icon: FileTextIcon },
  { name: 'Matches', to: '/matches', icon: UsersIcon },
];

export function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex flex-shrink-0 items-center">
              <BriefcaseIcon className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">CVision</span>
            </div>
            <div className="ml-6 flex space-x-8">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      'inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium',
                      {
                        'border-blue-500 text-gray-900': isActive,
                        'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700':
                          !isActive,
                      }
                    )
                  }
                >
                  <item.icon className="mr-2 h-4 w-4" />
                  {item.name}
                </NavLink>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}