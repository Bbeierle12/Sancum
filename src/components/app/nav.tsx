'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BookMarked, Users, LayoutDashboard, SearchCode, BrainCircuit } from 'lucide-react';

import {
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from '@/components/ui/sidebar';

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/journal', label: 'Journal', icon: BookMarked },
  { href: '/groups', label: 'Groups', icon: Users },
  { href: '/mirror-verse', label: 'Mirro-Verse', icon: SearchCode },
  { href: '/study-buddy', label: 'Study Buddy', icon: BrainCircuit },
];

export function Nav() {
  const pathname = usePathname();

  return (
    <SidebarMenu>
      {navItems.map((item) => (
        <SidebarMenuItem key={item.href}>
          <SidebarMenuButton
            asChild
            isActive={pathname === item.href}
            tooltip={item.label}
          >
            <Link href={item.href}>
              <item.icon />
              <span>{item.label}</span>
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>
      ))}
    </SidebarMenu>
  );
}
