
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Users } from 'lucide-react';

const groups = [
  { name: 'Morning Study Group', members: 12, image: 'https://placehold.co/40x40.png?text=M', hint: 'group people' },
  { name: 'Family Verses', members: 5, image: 'https://placehold.co/40x40.png?text=F', hint: 'family gathering' },
  { name: 'Covenant Path Companions', members: 8, image: 'https://placehold.co/40x40.png?text=C', hint: 'path mountain' },
];

export default function GroupsPage() {
  return (
    <div className="space-y-8">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold font-headline">Groups</h1>
          <p className="text-lg text-muted-foreground">
            Share verses and fulfillment logs with others.
          </p>
        </div>
        <Button>
          <Users className="mr-2 h-4 w-4" />
          Create Group
        </Button>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {groups.map((group) => (
          <Card key={group.name} className="shadow-lg">
            <CardHeader>
              <CardTitle className="font-headline">{group.name}</CardTitle>
              <CardDescription>{group.members} members</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex -space-x-2 overflow-hidden">
                {Array.from({ length: group.members > 5 ? 5 : group.members }).map((_, i) => (
                  <Avatar key={i} className="inline-block h-8 w-8 rounded-full ring-2 ring-background">
                    <AvatarImage src={`https://placehold.co/40x40.png?text=${i}`} data-ai-hint="person face" />
                    <AvatarFallback>U</AvatarFallback>
                  </Avatar>
                ))}
                 {group.members > 5 && <Avatar className="inline-block h-8 w-8 rounded-full ring-2 ring-background">
                    <AvatarFallback>+{group.members-5}</AvatarFallback>
                  </Avatar>}
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full">View Group</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
