'use client';

import { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';
import { Eye } from 'lucide-react';

type VerseCardProps = {
  reference: string;
  text: string;
  tags: string[];
};

export function VerseCard({ reference, text, tags }: VerseCardProps) {
  const { toast } = useToast();
  const [isRevealed, setIsRevealed] = useState(false);

  const handleReview = (quality: string) => {
    toast({
      title: 'Review Recorded',
      description: `You rated "${reference}" as "${quality}".`,
    });
    // In a real app, this would also reset the card state
  };

  const handleReveal = () => {
    setIsRevealed(true);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-lg">
      <CardHeader>
        <CardTitle className="font-headline text-3xl">{reference}</CardTitle>
        <CardDescription>From your scheduled review</CardDescription>
      </CardHeader>
      <CardContent className="min-h-[120px] flex items-center justify-center">
        {isRevealed ? (
          <div className="w-full">
            <p className="text-lg leading-relaxed">{text}</p>
            <Separator className="my-4" />
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <Badge key={tag} variant="secondary">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-muted-foreground italic">Try to recall the verse from memory.</p>
          </div>
        )}
      </CardContent>
      <CardFooter className="flex-col items-center gap-4 pt-6">
        {!isRevealed ? (
          <Button onClick={handleReveal}>
            <Eye />
            Reveal Verse
          </Button>
        ) : (
          <>
            <p className="text-sm text-muted-foreground">How well did you recall this verse?</p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 w-full max-w-md">
              <Button variant="outline" onClick={() => handleReview('Again')}>
                Again
              </Button>
              <Button variant="outline" onClick={() => handleReview('Hard')}>
                Hard
              </Button>
              <Button variant="outline" onClick={() => handleReview('Good')}>
                Good
              </Button>
              <Button variant="default" onClick={() => handleReview('Easy')}>
                Easy
              </Button>
            </div>
          </>
        )}
      </CardFooter>
    </Card>
  );
}
