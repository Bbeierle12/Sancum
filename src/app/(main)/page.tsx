import Link from 'next/link';
import { VerseCard } from '@/components/app/verse-card';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PenSquare, BrainCircuit, History } from 'lucide-react';

export default function DashboardPage() {
  const verseOfTheDay = {
    reference: 'John 3:16',
    text: '“For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.”',
    tags: ['Gospel', 'Atonement', 'Love', 'Faith'],
  };

  const reviewStats = {
    dueToday: 5,
    newToday: 2,
    totalMemorized: 150,
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Welcome to Sanctum</h1>
        <p className="text-lg text-muted-foreground">
          Your central hub for spiritual growth and reflection.
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div className="lg:col-span-2">
           <VerseCard
            reference={verseOfTheDay.reference}
            text={verseOfTheDay.text}
            tags={verseOfTheDay.tags}
          />
        </div>
        <div className="space-y-8">
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="font-headline flex items-center gap-2">
                <History className="text-primary"/>
                Review Summary
              </CardTitle>
              <CardDescription>Your spaced repetition progress.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
               <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Due Today</span>
                  <span className="font-bold">{reviewStats.dueToday} verses</span>
               </div>
               <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">New This Session</span>
                  <span className="font-bold">{reviewStats.newToday} verses</span>
               </div>
               <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Total Memorized</span>
                  <span className="font-bold">{reviewStats.totalMemorized} verses</span>
               </div>
            </CardContent>
          </Card>
           <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="font-headline">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <Button asChild variant="outline">
                <Link href="/journal">
                  <PenSquare />
                  <span>Add Journal Entry</span>
                </Link>
              </Button>
              <Button asChild variant="outline">
                <Link href="/study-buddy">
                  <BrainCircuit />
                  <span>Ask Study Buddy</span>
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
