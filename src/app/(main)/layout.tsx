import {
  SidebarProvider,
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarTrigger,
  SidebarInset,
} from '@/components/ui/sidebar';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Feather, CircleUserRound, Settings } from 'lucide-react';
import { Nav } from '@/components/app/nav';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarHeader>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="shrink-0">
              <Feather className="text-primary" />
            </Button>
            <h1 className="text-xl font-semibold font-headline">Sanctum</h1>
          </div>
        </SidebarHeader>
        <SidebarContent>
          <Nav />
        </SidebarContent>
        <SidebarFooter>
          <div className="flex items-center gap-3">
             <Avatar className="h-8 w-8">
              <AvatarImage src="https://placehold.co/40x40.png" alt="User" data-ai-hint="person face" />
              <AvatarFallback>U</AvatarFallback>
            </Avatar>
            <div className="flex-1 overflow-hidden">
                <p className="font-semibold text-sm truncate">User Name</p>
            </div>
            <Button variant="ghost" size="icon">
                <Settings />
            </Button>
          </div>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <header className="p-4 flex items-center gap-4 md:hidden border-b">
          <SidebarTrigger />
          <div className="flex items-center gap-2">
            <Feather className="text-primary h-6 w-6" />
            <h1 className="text-lg font-semibold font-headline">Sanctum</h1>
          </div>
        </header>
        <main className="flex-1 p-4 md:p-8 bg-background">
            {children}
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
